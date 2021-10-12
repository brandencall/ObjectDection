import numpy as np
import cv2 as cv
import win32gui
import win32ui
import win32con

'''

Used code from https://github.com/learncodebygaming/opencv_tutorials/blob/master/004_window_capture/windowcapture.py and
https://stackoverflow.com/questions/59350839/capturing-screenshots-with-win32api-python-returns-black-image 

'''


class WindowCapture:

    # properties
    w = 0
    h = 0
    hwnd_target = None
    # Values specific for Dino run game
    cropped_x = 400
    cropped_y = 400
    offset_x = 0
    offset_y = 0

    # constructor
    def __init__(self, window_name):
        # find the handle for the window we want to capture
        self.hwnd_target = win32gui.FindWindow(None, window_name)
        # win32gui.SetForegroundWindow(hwnd_target)
        if not self.hwnd_target:
            raise Exception('Window not found: {}'.format(self.hwnd_target))

        # get the window size
        window_rect = win32gui.GetWindowRect(self.hwnd_target)
        # -250 is specific for dino run game
        self.w = window_rect[2] - window_rect[0] - 250
        self.h = window_rect[3] - window_rect[1] - 250

        # account for the window border and titlebar and cut them off
        # border_pixels = 200
        # titlebar_pixels = 200
        # self.w = self.w - (border_pixels * 2)
        # self.h = self.h - titlebar_pixels - border_pixels
        # self.cropped_x = border_pixels
        # self.cropped_y = titlebar_pixels

        # set the cropped coordinates offset so we can translate screenshot
        # images into actual screen positions
        self.offset_x = window_rect[0] + self.cropped_x
        self.offset_y = window_rect[1] + self.cropped_y

    def get_screenshot(self):

        # get the window image data
        hdesktop = win32gui.GetDesktopWindow()

        hwndDC = win32gui.GetWindowDC(hdesktop)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()

        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, self.w, self.h)

        saveDC.SelectObject(saveBitMap)

        result = saveDC.BitBlt((0, 0), (self.w, self.h), mfcDC,
                               (self.cropped_x, self.cropped_y), win32con.SRCCOPY)

        # convert the raw data into a format opencv can read
        #dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')
        signedIntsArray = saveBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        # img = cv.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # img = cv.Canny(img, threshold1=119, threshold2=250)
        img.shape = (self.h, self.w, 4)

        # free resources
        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(hdesktop, hwndDC)

        # drop the alpha channel, or cv.matchTemplate() will throw an error like:
        #   error: (-215:Assertion failed) (depth == CV_8U || depth == CV_32F) && type == _templ.type()
        #   && _img.dims() <= 2 in function 'cv::matchTemplate'
        img = img[..., :4]

        # make image C_CONTIGUOUS to avoid errors that look like:
        #   File ... in draw_rectangles
        #   TypeError: an integer is required (got type tuple)
        # see the discussion here:
        # https://github.com/opencv/opencv/issues/14866#issuecomment-580207109
        img = np.ascontiguousarray(img)

        return img

    # find the name of the window you're interested in.
    # once you have it, update window_capture()
    # https://stackoverflow.com/questions/55547940/how-to-get-a-list-of-the-name-of-every-open-window
    @staticmethod
    def list_window_names():
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler, None)


# translate a pixel position on a screenshot image to a pixel position on the screen.
# pos = (x, y)
# WARNING: if you move the window being captured after execution is started, this will
# return incorrect coordinates, because the window position is only calculated in
# the __init__ constructor.


def get_screen_position(self, pos):
    return (pos[0] + self.offset_x, pos[1] + self.offset_y)
