// Think the 'delete log full' duz a reset....
function LogData () {
    datalogger.log(
    datalogger.createCV("temp", input.temperature()),
    datalogger.createCV("light", input.lightLevel()),
    datalogger.createCV("sound", input.soundLevel()),
    datalogger.createCV("soil", Soil)
    )
}
datalogger.onLogFull(function () {
    basic.showIcon(IconNames.Sad)
})
input.onLogoEvent(TouchButtonEvent.LongPressed, function () {
    basic.showIcon(IconNames.Ghost)
    LogData()
    basic.clearScreen()
})
input.onButtonPressed(Button.A, function () {
    music.play(music.tonePlayable(100 * input.temperature(), music.beat(BeatFraction.Whole)), music.PlaybackMode.InBackground)
    basic.showIcon(IconNames.TShirt)
    basic.showNumber(input.temperature())
    changeSoundLevel(-10)
})
function SoilRead () {
    pins.digitalWritePin(DigitalPin.P1, 1)
    basic.pause(1)
    Soil = pins.analogReadPin(AnalogPin.P0)
    pins.digitalWritePin(DigitalPin.P1, 0)
}
function changeSoundLevel (delta: number) {
    basic.clearScreen()
    level += delta
    input.setSoundThreshold(SoundThreshold.Loud, level)
}
input.onSound(DetectedSound.Loud, function () {
    music.play(music.createSoundExpression(WaveShape.Sine, 5000, 0, 255, 0, 2984, SoundExpressionEffect.Warble, InterpolationCurve.Logarithmic), music.PlaybackMode.InBackground)
    basic.showIcon(IconNames.Chessboard)
    changeSoundLevel(-1)
    basic.showNumber(input.soundLevel())
    basic.showIcon(IconNames.EighthNote)
    basic.showNumber(level)
    basic.clearScreen()
})
input.onButtonPressed(Button.AB, function () {
    datalogger.deleteLog(datalogger.DeleteType.Full)
    basic.showString("Log Gone!")
    basic.clearScreen()
    LogCols()
    SoilRead()
    LogData()
})
input.onButtonPressed(Button.B, function () {
    music.play(music.tonePlayable(Soil, music.beat(BeatFraction.Whole)), music.PlaybackMode.InBackground)
    SoilRead()
    basic.showIcon(IconNames.SmallSquare)
    basic.showNumber(Soil)
    changeSoundLevel(10)
})
function LogCols () {
    datalogger.includeTimestamp(FlashLogTimeStampFormat.Minutes)
    datalogger.setColumnTitles(
    "temp",
    "light",
    "sound",
    "soil"
    )
}
input.onLogoEvent(TouchButtonEvent.Pressed, function () {
    music.play(music.tonePlayable(level, music.beat(BeatFraction.Whole)), music.PlaybackMode.InBackground)
    basic.showIcon(IconNames.EighthNote)
    basic.showNumber(level)
    basic.clearScreen()
})
let Soil = 0
let level = 0
led.setBrightness(64)
music.setVolume(53)
level = 170
input.setSoundThreshold(SoundThreshold.Loud, level)
basic.showIcon(IconNames.Happy)
LogCols()
loops.everyInterval(1200000, function () {
    SoilRead()
    LogData()
    basic.showNumber(input.temperature())
    basic.showIcon(IconNames.SmallDiamond)
    basic.showNumber(input.lightLevel())
    basic.showIcon(IconNames.SmallSquare)
    basic.showNumber(Soil)
    basic.clearScreen()
})
