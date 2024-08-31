"""

Think the 'delete log full' duz a reset....

"""
def LogData():
    datalogger.log(datalogger.create_cv("temp", input.temperature()),
        datalogger.create_cv("light", input.light_level()),
        datalogger.create_cv("sound", input.sound_level()),
        datalogger.create_cv("soil", Soil))

def on_log_full():
    basic.show_icon(IconNames.SAD)
datalogger.on_log_full(on_log_full)

def on_logo_long_pressed():
    basic.show_icon(IconNames.GHOST)
    LogData()
    basic.clear_screen()
input.on_logo_event(TouchButtonEvent.LONG_PRESSED, on_logo_long_pressed)

def on_button_pressed_a():
    music.play(music.tone_playable(100 * input.temperature(), music.beat(BeatFraction.WHOLE)),
        music.PlaybackMode.IN_BACKGROUND)
    basic.show_icon(IconNames.TSHIRT)
    basic.show_number(input.temperature())
    changeSoundLevel(-10)
input.on_button_pressed(Button.A, on_button_pressed_a)

def SoilRead():
    global Soil
    pins.digital_write_pin(DigitalPin.P1, 1)
    basic.pause(1)
    Soil = pins.analog_read_pin(AnalogPin.P0)
    pins.digital_write_pin(DigitalPin.P1, 0)
def changeSoundLevel(delta: number):
    global level
    basic.clear_screen()
    level += delta
    input.set_sound_threshold(SoundThreshold.LOUD, level)

def on_sound_loud():
    music.play(music.create_sound_expression(WaveShape.SINE,
            5000,
            0,
            255,
            0,
            2984,
            SoundExpressionEffect.WARBLE,
            InterpolationCurve.LOGARITHMIC),
        music.PlaybackMode.IN_BACKGROUND)
    basic.show_icon(IconNames.CHESSBOARD)
    changeSoundLevel(-1)
    basic.show_number(input.sound_level())
    basic.show_icon(IconNames.EIGHTH_NOTE)
    basic.show_number(level)
    basic.clear_screen()
input.on_sound(DetectedSound.LOUD, on_sound_loud)

def on_button_pressed_ab():
    datalogger.delete_log(datalogger.DeleteType.FULL)
    basic.show_string("Log Gone!")
    basic.clear_screen()
    LogCols()
    SoilRead()
    LogData()
input.on_button_pressed(Button.AB, on_button_pressed_ab)

def on_button_pressed_b():
    music.play(music.tone_playable(Soil, music.beat(BeatFraction.WHOLE)),
        music.PlaybackMode.IN_BACKGROUND)
    SoilRead()
    basic.show_icon(IconNames.SMALL_SQUARE)
    basic.show_number(Soil)
    changeSoundLevel(10)
input.on_button_pressed(Button.B, on_button_pressed_b)

def LogCols():
    datalogger.include_timestamp(FlashLogTimeStampFormat.MINUTES)
    datalogger.set_column_titles("temp", "light", "sound", "soil")

def on_logo_pressed():
    music.play(music.tone_playable(level, music.beat(BeatFraction.WHOLE)),
        music.PlaybackMode.IN_BACKGROUND)
    basic.show_icon(IconNames.EIGHTH_NOTE)
    basic.show_number(level)
    basic.clear_screen()
input.on_logo_event(TouchButtonEvent.PRESSED, on_logo_pressed)

Soil = 0
level = 0
led.set_brightness(64)
music.set_volume(53)
level = 170
input.set_sound_threshold(SoundThreshold.LOUD, level)
basic.show_icon(IconNames.HAPPY)
LogCols()

def on_every_interval():
    SoilRead()
    LogData()
    basic.show_number(input.temperature())
    basic.show_icon(IconNames.SMALL_DIAMOND)
    basic.show_number(input.light_level())
    basic.show_icon(IconNames.SMALL_SQUARE)
    basic.show_number(Soil)
    basic.clear_screen()
loops.every_interval(1200000, on_every_interval)
