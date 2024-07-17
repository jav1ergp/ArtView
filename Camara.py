import cv2
import numpy as np
import cuia
import test

# Diccionario de marcadores Aruco
diccionario = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)

# Detector de ArUco
detector = cv2.aruco.ArucoDetector(diccionario)

def origen(TAM):
    return(np.array([[-TAM/2.0, -TAM/2.0, 0.0],
                     [-TAM/2.0,  TAM/2.0, 0.0],
                     [ TAM/2.0,  TAM/2.0, 0.0],
                     [ TAM/2.0, -TAM/2.0, 0.0]]))

def proyeccion(puntos, rvec, tvec, cameraMatrix, distCoeffs):
    puntos = np.array(puntos, dtype=np.float32)
    if puntos.ndim == 1 and puntos.size == 3:
        puntos = np.expand_dims(puntos, axis=0)
    res, _ = cv2.projectPoints(puntos, rvec, tvec, cameraMatrix, distCoeffs)
    return res.reshape(-1, 2)

def detectar_aruco(frame, imagen_proyectar):
    TAM = 0.2
    imagen_proyectar_bgra = cv2.cvtColor(imagen_proyectar, cv2.COLOR_BGR2BGRA)
    hframe, wframe, _ = frame.shape
    bboxs, ids, _ = detector.detectMarkers(frame)
    if ids is not None:
        frame_bgra = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
        for i in range(len(ids)):
            #if ids[i][0] == 1:  # Proyectar solo el marcador con ID 1
            ret, rvec, tvec = cv2.solvePnP(origen(TAM), bboxs[i], test.cameraMatrix, test.distCoeffs)
            if ret:
                h, w, _ = imagen_proyectar_bgra.shape
                desde = np.array([[0, 0], [w, 0], [w, h], [0, h]], dtype=np.float32)
                hasta = proyeccion(origen(TAM), rvec, tvec, test.cameraMatrix, test.distCoeffs)
                M = cv2.getPerspectiveTransform(np.float32(desde), np.float32(hasta))
                warp = cv2.warpPerspective(imagen_proyectar_bgra, M, dsize=(wframe,hframe))
                frame_bgra = cuia.alphaBlending(warp, frame_bgra)
        frame = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)
    return frame
