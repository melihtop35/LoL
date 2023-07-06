import cv2
import numpy as np
import pyautogui
import schedule
import keyboard
import sys

screenWidth = 0
screenHeight = 0


def DONGU():
    global screenWidth, screenHeight
    screenWidth, screenHeight = pyautogui.size()
    ekranGörüntüsü = pyautogui.screenshot()
    resim = "resim.png"
    ekranGörüntüsü.save(resim)

    resim = cv2.imread("resim.png")
    resim_gri = cv2.cvtColor(resim, cv2.COLOR_BGR2GRAY)

    ara_resim = cv2.imread("aranan.png")
    ara_resim_gri = cv2.cvtColor(ara_resim, cv2.COLOR_BGR2GRAY)

    eslesme = cv2.matchTemplate(resim_gri, ara_resim_gri, cv2.TM_CCOEFF_NORMED)
    loc = np.where(eslesme >= 0.5)

    if len(loc[0]) > 0:
        for pt in zip(*loc[::-1]):
            screen_center = (
                pt[0] + ara_resim.shape[1] // 2,
                pt[1] + ara_resim.shape[0] // 2,
            )

            # Bulunan bölgede kabulEt.png'yi arayın.
            kabul_et = cv2.imread("kabulEt.png")
            kabul_et_gri = cv2.cvtColor(kabul_et, cv2.COLOR_BGR2GRAY)

            kabul_et_eslesme = cv2.matchTemplate(
                ara_resim_gri, kabul_et_gri, cv2.TM_CCOEFF_NORMED
            )
            loc_kabul_et = np.where(kabul_et_eslesme >= 0.5)

            if len(loc_kabul_et[0]) > 0:
                for pt_kabul_et in zip(*loc_kabul_et[::-1]):
                    kabul_et_center = (
                        pt[0] + pt_kabul_et[0] + kabul_et.shape[1] // 2,
                        pt[1] + pt_kabul_et[1] + kabul_et.shape[0],
                    )
                    pyautogui.click(kabul_et_center)
                    sys.exit()  # Programı tamamen durdur.
                break
            break


def main():
    global screenWidth, screenHeight
    print("Başladı")
    screenWidth, screenHeight = pyautogui.size()
    schedule.every(1).seconds.do(DONGU)

    while True:
        schedule.run_pending()
        if keyboard.is_pressed("ESC"):  # ESC tuşu ile döngüden çık.
            sys.exit()  # Programı tamamen durdur.


main()
