import base64
import cv2
import numpy as np

from skimage.metrics import structural_similarity as ssim
from skimage.feature import local_binary_pattern
from ..schemas.SignatureSchema import SaveSignature, OwnerSignature, UpdateSignature, UpdatedSignature, VerifySignature
from ..cruds.SignatureCrud import create_signature, get_list_signature, update_signature
from asyncpg import Connection

async def castImageToBase64(imageFile):
    imageBytes = await imageFile.read()
    castImageToBase64 = base64.b64encode(imageBytes).decode(encoding='ascii')
    return castImageToBase64

def decodeToVerify(base64Image): 
    imageData = base64.b64decode(base64Image)
    np_arr = np.frombuffer(imageData, np.uint8)
    return cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)

async def getListSignature(conn : Connection):
    records = await get_list_signature(conn)
    signatureList = [SaveSignature(full_name=record['full_name'], image_signature=record['image_signature']) for record in records]
    return signatureList

async def createSignature(conn : Connection, owner : OwnerSignature):
    base64Image = await castImageToBase64(owner.image_signature)
    saveSignature = SaveSignature(
        full_name=owner.full_name,
        image_signature=base64Image
    )
    result = await create_signature(conn, saveSignature)
    return result

async def updateSignature(conn : Connection, owner : UpdateSignature):
    base64Image = await castImageToBase64(owner.image_signature)
    updateSignature = UpdatedSignature(stt=owner.stt, 
                                       image_signature=base64Image)
    result = await update_signature(conn, updateSignature)
    return result


def preprocessSignature(image):
    # Làm mờ để giảm nhiễu
    image = cv2.GaussianBlur(image, (3, 3), 0) # (3,3) Kích thước kernel, 0 = độ lệch chuẩn Kernel = ma trận để tính toán
    # Cân bằng độ sáng
    image = cv2.equalizeHist(image)
    # Chuyển ảnh thành nhị phân
    binary = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11 ,2)
    # Tạo kernel (ma trận nhỏ) để xử lý
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    # MORPH_CLOSE lắp đầy các khoảng trống nhỏ
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    # MORPH_OPEN: loại bỏ nhiễu nhỏ
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    return binary

def templateMatching(img1, img2):
    """Template matching với nhiều tỷ lệ"""
    try:
        maxScore = 0
        for scale in [0.8, 0.9, 1.0, 1.1, 1.2]:
            resized = cv2.resize(img2, None, fx=scale, fy=scale)
            if resized.shape[0] <= img1.shape[0] and resized.shape[1] <= img1.shape[1]:
                result = cv2.matchTemplate(img1, resized, cv2.TM_CCOEFF_NORMED)
                _, maxVal, _, _ = cv2.minMaxLoc(result)
                maxScore = max(maxScore, maxVal)
        return maxScore
    except:
        return None

def compareLBPFeatures(img1, img2):
    """So sánh đặc trưng LBP"""
    try:
        radius = 3
        nPoints = 8 * radius
        lbp1 = local_binary_pattern(img1, nPoints, radius, method='uniform')
        lbp2 = local_binary_pattern(img2, nPoints, radius, method='uniform')
        hist1, _ = np.histogram(lbp1.ravel(), bins=nPoints + 2, range=(0, nPoints + 2))
        hist2, _ = np.histogram(lbp2.ravel(), bins=nPoints + 2, range=(0, nPoints + 2))
        
        hist1 = hist1.astype(float)
        hist2 = hist2.astype(float)
        hist1 /= (hist1.sum() + 1e-7)
        hist2 /= (hist2.sum() + 1e-7)
        
        correlation = np.corrcoef(hist1, hist2)[0,1]
        return max(0, correlation)

    except:
        return None

def compareContours(img1, img2):
    """So sánh đường viền chữ ký"""
    try:
        contours1, _ = cv2.findContours(img1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours2, _ = cv2.findContours(img2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours1 or not contours2:
            return None
        
        c1 = max(contours1, key=cv2.contourArea)
        c2 = max(contours2, key=cv2.contourArea)
        # Tính Hu moments
        moments1 = cv2.moments(c1)
        moments2 = cv2.moments(c2)    

        hu1 = cv2.HuMoments(moments1).flatten()
        hu2 = cv2.HuMoments(moments2).flatten()

        similarity = 1 - np.mean(np.abs(hu1 - hu2))
        return max(0, similarity)
    except: 
        None

def calculateCombinedScore(img1, img2): 
    scores = []
    weights = []

    try: 
        ssim_score = ssim(img1, img2, data_range=255)
        scores.append(ssim_score)
        weights.append(0.4)
    except: 
        pass

    # 2. Template score matching voi nhieu scale 
    template_score = templateMatching(img1, img2)
    if template_score is not None: 
        scores.append(template_score)
        weights.append(0.25)
    
    # 3. LBP(Local binary pattern)
    lbp_scores = compareLBPFeatures(img1,img2)
    if lbp_scores is not None: 
        scores.append(lbp_scores)
        weights.append(0.2)

    # 4. Contour Matching
    contour_scores = compareContours(img1, img2)
    if contour_scores is not None:
        scores.append(contour_scores)
        weights.append(0.15)
    
    if scores:
        total_weights = sum(weights)
        weight_score = sum(s * w for s, w in zip(scores, weights)) / total_weights
        return weight_score
    return 0


async def verifySignature(conn : Connection, verify : VerifySignature):
    castImageToBytes = await verify.image.read()
    np_arr = np.frombuffer(castImageToBytes, np.uint8)
    verifyImage = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)
    verifyImage = cv2.resize(verifyImage, (300,100))
    verifyImage = preprocessSignature(verifyImage)

    listSignature = await get_list_signature(conn)
    thresHold = 0.5

    bestFit = None
    highestScore = 0

    for record in listSignature: 
        signatureSaved = decodeToVerify(record['image_signature'])
        signatureSaved = cv2.resize(signatureSaved, (300,100))
        signatureSaved = preprocessSignature(signatureSaved)
        
        finalScore = calculateCombinedScore(verifyImage, signatureSaved)
        if finalScore > highestScore: 
            highestScore = finalScore
            bestFit = record
    
    if highestScore >= thresHold: 
        return {
            'match': True,
            'fullName': bestFit['full_name'],
            'confidence': round(highestScore, 2)
        }
    return {
        'match': False,
        'message': 'Not found'
    }