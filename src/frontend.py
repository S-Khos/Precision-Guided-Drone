import cv2
import time
import math
import numpy as np


class FrontEnd(object):

    def __init__(self, state):
        self.state = state
        self.fps_init_time = time.time()

    def update(self):
        self.state.UI_COLOUR = self.state.GREEN if self.state.RBG else self.state.WHITE
        # fps
        elapsed_time = time.time() - self.fps_init_time
        fps = int(1 / elapsed_time)
        self.fps_init_time = time.time()
        fps_size = cv2.getTextSize("FPS  {}".format(
            fps), self.state.FONT, self.state.FONT_SCALE, self.state.LINE_THICKNESS)[0][0]
        self.state.frame = cv2.putText(self.state.frame, "FPS  {}".format(fps), (self.state.FRAME_WIDTH -
                                                                                 fps_size - 5, 25), self.state.FONT, self.state.FONT_SCALE, self.state.UI_COLOUR, self.state.LINE_THICKNESS)

        # top left
        self.state.frame = cv2.putText(self.state.frame, "PWR   {}%".format(self.state.battery),
                                       (5, 25), self.state.FONT, self.state.FONT_SCALE, self.state.UI_COLOUR, self.state.LINE_THICKNESS)
        self.state.frame = cv2.putText(self.state.frame, "TMP  {}C".format(self.state.temperature),
                                       (5, 55), self.state.FONT, self.state.FONT_SCALE, self.state.UI_COLOUR, self.state.LINE_THICKNESS)

        # crosshair
        self.state.frame = cv2.line(self.state.frame, (self.state.CENTRE_X - 20, self.state.CENTRE_Y),
                                    (self.state.CENTRE_X - 10, self.state.CENTRE_Y), self.state.UI_COLOUR, 2)
        self.state.frame = cv2.line(self.state.frame, (self.state.CENTRE_X + 20, self.state.CENTRE_Y),
                                    (self.state.CENTRE_X + 10, self.state.CENTRE_Y), self.state.UI_COLOUR, 2)
        self.state.frame = cv2.line(self.state.frame, (self.state.CENTRE_X, self.state.CENTRE_Y - 20),
                                    (self.state.CENTRE_X, self.state.CENTRE_Y - 10), self.state.UI_COLOUR, 2)
        self.state.frame = cv2.line(self.state.frame, (self.state.CENTRE_X, self.state.CENTRE_Y + 20),
                                    (self.state.CENTRE_X, self.state.CENTRE_Y + 10), self.state.UI_COLOUR, 2)

        # crosshair stats
        spd_size = cv2.getTextSize("SPD  {:.1f} FT/S".format(np.hypot(self.state.x_speed, self.state.y_speed)),
                                   self.state.FONT, self.state.FONT_SCALE, self.state.LINE_THICKNESS)[0][0]
        self.state.frame = cv2.putText(self.state.frame, "SPD  {:.1f} FT/S".format(np.hypot(self.state.x_speed, self.state.y_speed)), ((self.state.CENTRE_X) - 140 - spd_size + spd_size // 2,
                                       (self.state.CENTRE_Y) - 100), self.state.FONT, self.state.FONT_SCALE, self.state.UI_COLOUR, self.state.LINE_THICKNESS)

        alt_size = cv2.getTextSize("ALT  {:.1f} FT".format(self.state.altitude),
                                   self.state.FONT, self.state.FONT_SCALE, self.state.LINE_THICKNESS)[0][0]

        self.state.frame = cv2.putText(self.state.frame, "ALT  {:.1f} FT".format(self.state.altitude), ((
            self.state.CENTRE_X) + 130 - alt_size + alt_size // 2, (self.state.CENTRE_Y) - 100), self.state.FONT, self.state.FONT_SCALE, self.state.UI_COLOUR, self.state.LINE_THICKNESS)

        if not self.state.RBG:
            flir_size = cv2.getTextSize(
                "GRAY", self.state.FONT, self.state.FONT_SCALE, self.state.LINE_THICKNESS)[0][0]
            self.state.frame = cv2.putText(self.state.frame, "GRAY",
                                           ((self.state.CENTRE_X) - 140 - flir_size + flir_size // 2,
                                            (self.state.CENTRE_Y) + 100), self.state.FONT, self.state.FONT_SCALE, self.state.UI_COLOUR, self.state.LINE_THICKNESS)

        # bottom left telemtry
        self.state.frame = cv2.putText(self.state.frame, "BRM  {}".format(self.state.barometer), (
            5, self.state.FRAME_HEIGHT - 130), self.state.FONT, self.state.FONT_SCALE, self.state.UI_COLOUR, self.state.LINE_THICKNESS)
        self.state.frame = cv2.putText(self.state.frame, "THR  {}  {}  {}".format(self.state.yaw_Throttle, self.state.lr_Throttle, 0), (
            5, self.state.FRAME_HEIGHT - 100), self.state.FONT, self.state.FONT_SCALE, self.state.UI_COLOUR, self.state.LINE_THICKNESS)
        self.state.frame = cv2.putText(self.state.frame, "SPD  {:.1f}  {:.1f}  {:.1f}".format(self.state.x_speed, self.state.y_speed, self.state.z_speed), (5,
                                                                                                                                                            self.state.FRAME_HEIGHT - 70), self.state.FONT, self.state.FONT_SCALE, self.state.UI_COLOUR, self.state.LINE_THICKNESS)
        self.state.frame = cv2.putText(self.state.frame, "ACC  {}  {}  {}".format(self.state.acceleration_x, self.state.acceleration_y, self.state.acceleration_z),
                                       (5, self.state.FRAME_HEIGHT - 40), self.state.FONT, self.state.FONT_SCALE, self.state.UI_COLOUR, self.state.LINE_THICKNESS)
        self.state.frame = cv2.putText(self.state.frame, "YPR  {}  {}  {}".format(self.state.yaw, self.state.pitch, self.state.roll), (5,
                                                                                                                                       self.state.FRAME_HEIGHT - 10), self.state.FONT, self.state.FONT_SCALE, self.state.UI_COLOUR, self.state.LINE_THICKNESS)

        time_size = cv2.getTextSize(
            "T + {}".format(self.state.flight_time), self.state.FONT, self.state.FONT_SCALE, self.state.LINE_THICKNESS)[0][0]
        self.state.frame = cv2.putText(self.state.frame, "T + {}".format(self.state.flight_time),
                                       (self.state.FRAME_WIDTH - time_size - 5, 55), self.state.FONT, self.state.FONT_SCALE, self.state.UI_COLOUR, self.state.LINE_THICKNESS)

        # bottom compass
        self.state.frame = cv2.circle(self.state.frame, (self.state.FRAME_WIDTH - 60, self.state.FRAME_HEIGHT - 60),
                                      50, self.state.UI_COLOUR, 1)
        self.state.frame = cv2.arrowedLine(self.state.frame, (self.state.FRAME_WIDTH - 60, self.state.FRAME_HEIGHT - 60), (int(-50 * math.cos(math.radians(self.state.yaw + 90)) +
                                                                                                                               self.state.FRAME_WIDTH - 60), int((self.state.FRAME_HEIGHT - 60) - (50 * math.sin(math.radians(self.state.yaw + 90))))), self.state.UI_COLOUR, 1, tipLength=.15)

        # top center
        if (self.state.KC_manual and not self.state.GS_active):
            self.state.frame = cv2.rectangle(self.state.frame, (self.state.CENTRE_X - 20, 5),
                                             (self.state.CENTRE_X + 37, 30), self.state.UI_COLOUR, -1)
            self.state.frame = cv2.putText(self.state.frame, "CTRL", (self.state.CENTRE_X - 20, 25),
                                           self.state.FONT, self.state.FONT_SCALE, self.state.BLACK, self.state.LINE_THICKNESS)
        else:
            self.state.frame = cv2.rectangle(self.state.frame, (self.state.CENTRE_X - 20, 5),
                                             (self.state.CENTRE_X + 37, 30), self.state.UI_COLOUR, -1)
            self.state.frame = cv2.putText(self.state.frame, "AUTO", (self.state.CENTRE_X - 20, 25),
                                           self.state.FONT, self.state.FONT_SCALE, self.state.BLACK, self.state.LINE_THICKNESS)

        # designator cursor
        if not self.state.TR_active and self.state.TR_reset:
            self.state.frame = cv2.rectangle(self.state.frame, (self.state.CC_cursor_pos[0], self.state.CC_cursor_pos[1]), (
                self.state.CC_cursor_pos[0] + self.state.KC_designator_roi_size[0], self.state.CC_cursor_pos[1] + self.state.KC_designator_roi_size[1]), self.state.UI_COLOUR, 1)
            # top
            self.state.frame = cv2.line(self.state.frame, (self.state.CC_cursor_pos[0] + self.state.KC_designator_roi_size[0] // 2, self.state.CC_cursor_pos[1]),
                                        (self.state.CC_cursor_pos[0] + self.state.KC_designator_roi_size[0] // 2, 0), self.state.UI_COLOUR, 1)
            # left
            self.state.frame = cv2.line(self.state.frame, (self.state.CC_cursor_pos[0], self.state.CC_cursor_pos[1] + self.state.KC_designator_roi_size[1] // 2),
                                        (0, self.state.CC_cursor_pos[1] + self.state.KC_designator_roi_size[1] // 2), self.state.UI_COLOUR, 1)
            # right
            self.state.frame = cv2.line(self.state.frame, (self.state.CC_cursor_pos[0] + self.state.KC_designator_roi_size[0], self.state.CC_cursor_pos[1] + self.state.KC_designator_roi_size[1] // 2),
                                        (self.state.FRAME_WIDTH, self.state.CC_cursor_pos[1] + self.state.KC_designator_roi_size[1] // 2), self.state.UI_COLOUR, 1)
            # bottom
            self.state.frame = cv2.line(self.state.frame, (self.state.CC_cursor_pos[0] + self.state.KC_designator_roi_size[0] // 2, self.state.CC_cursor_pos[1] + self.state.KC_designator_roi_size[1]),
                                        (self.state.CC_cursor_pos[0] + self.state.KC_designator_roi_size[0] // 2, self.state.FRAME_HEIGHT), self.state.UI_COLOUR, 1)

        # active tracking / lock
        if self.state.TR_active and self.state.TR_return:
            x, y, w, h = int(self.state.TR_bbox[0]), int(self.state.TR_bbox[1]), int(
                self.state.TR_bbox[2]), int(self.state.TR_bbox[3])

            if self.state.GS_dive:
                dive_size = cv2.getTextSize(
                    "DIVE", self.state.FONT, self.state.FONT_SCALE, self.state.LINE_THICKNESS)[0][0]

                self.state.frame = cv2.rectangle(self.state.frame, (self.state.CENTRE_X - (dive_size // 2), self.state.FRAME_HEIGHT - 74),
                                                 (self.state.CENTRE_X + dive_size - 25, self.state.FRAME_HEIGHT - 53), self.state.UI_COLOUR, -1)

                self.state.frame = cv2.putText(self.state.frame, "DIVE", (self.state.CENTRE_X - (dive_size // 2),
                                                                          self.state.FRAME_HEIGHT - 53), self.state.FONT, self.state.FONT_SCALE, self.state.BLACK, self.state.LINE_THICKNESS)

            if (self.state.CENTRE_X > x and self.state.CENTRE_X < x + w and self.state.CENTRE_Y > y and self.state.CENTRE_Y < y + h and self.state.GS_dive):
                self.state.GS_lock = True

                lock_size = cv2.getTextSize(
                    "LOCK", self.state.FONT, self.state.FONT_SCALE, self.state.LINE_THICKNESS)[0][0]
                self.state.frame = cv2.rectangle(self.state.frame, (self.state.CENTRE_X - (lock_size // 2), self.state.FRAME_HEIGHT - 43),
                                                 (self.state.CENTRE_X + lock_size - 29, self.state.FRAME_HEIGHT - 17), self.state.UI_COLOUR, -1)

                self.state.frame = cv2.putText(self.state.frame, "LOCK", (self.state.CENTRE_X - (lock_size // 2),
                                                                          self.state.FRAME_HEIGHT - 22), self.state.FONT, self.state.FONT_SCALE, self.state.BLACK, self.state.LINE_THICKNESS)
            else:
                self.state.GS_lock = False
                trk_size = cv2.getTextSize(
                    "TRK", self.state.FONT, self.state.FONT_SCALE, self.state.LINE_THICKNESS)[0][0]
                self.state.frame = cv2.rectangle(self.state.frame, (self.state.CENTRE_X - (trk_size // 2), self.state.FRAME_HEIGHT - 41),
                                                 (self.state.CENTRE_X + trk_size - 20, self.state.FRAME_HEIGHT - 20), self.state.UI_COLOUR, -1)
                self.state.frame = cv2.putText(self.state.frame, "TRK", (self.state.CENTRE_X - (trk_size // 2),
                                                                         self.state.FRAME_HEIGHT - 22), self.state.FONT, self.state.FONT_SCALE, self.state.BLACK, self.state.LINE_THICKNESS)

            self.state.frame = cv2.line(self.state.frame, (x, y), (x + ((w) // 4), y),
                                        self.state.RED if self.state.GS_lock else self.state.UI_COLOUR, 2)
            self.state.frame = cv2.line(self.state.frame, (x, y), (x, y + ((h) // 4)),
                                        self.state.RED if self.state.GS_lock else self.state.UI_COLOUR, 2)
            self.state.frame = cv2.line(self.state.frame, (x, y + h), (x, y + h - ((h) // 4)),
                                        self.state.RED if self.state.GS_lock else self.state.UI_COLOUR, 2)
            self.state.frame = cv2.line(self.state.frame, (x, y + h), (x + ((w) // 4), y + h),
                                        self.state.RED if self.state.GS_lock else self.state.UI_COLOUR, 2)

            self.state.frame = cv2.line(self.state.frame, (x + w, y), (x + w - ((w) // 4), y),
                                        self.state.RED if self.state.GS_lock else self.state.UI_COLOUR, 2)
            self.state.frame = cv2.line(self.state.frame, (x + w, y), (x + w, y + ((h) // 4)),
                                        self.state.RED if self.state.GS_lock else self.state.UI_COLOUR, 2)
            self.state.frame = cv2.line(self.state.frame, (x + w, y + h), (x + w, y + h - ((h) // 4)),
                                        self.state.RED if self.state.GS_lock else self.state.UI_COLOUR, 2)
            self.state.frame = cv2.line(self.state.frame, (x + w, y + h), (x + w - ((w) // 4), y + h),
                                        self.state.RED if self.state.GS_lock else self.state.UI_COLOUR, 2)

            self.state.frame = cv2.circle(self.state.frame, (x + w // 2, y + h // 2), 3,
                                          self.state.RED if self.state.GS_lock else self.state.UI_COLOUR, -1)
            # top
            self.state.frame = cv2.line(self.state.frame, (x + w // 2, y),
                                        (x + w // 2, 0), self.state.UI_COLOUR, 1)
            # left
            self.state.frame = cv2.line(self.state.frame, (x, y + h // 2),
                                        (0, y + h // 2), self.state.UI_COLOUR, 1)
            # right
            self.state.frame = cv2.line(self.state.frame, (x + w, y + h // 2),
                                        (self.state.FRAME_WIDTH, y + h // 2), self.state.UI_COLOUR, 1)
            # bottom
            self.state.frame = cv2.line(self.state.frame, (x + w // 2, y + h),
                                        (x + w // 2, self.state.FRAME_HEIGHT), self.state.UI_COLOUR, 1)
