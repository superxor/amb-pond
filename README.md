# POND

A generative garden pond for the [M-VAVE FM-1](https://github.com/charlesvestal/fm1-base). Switch it on and it is already playing: breathing voices, drops on loops of unequal length, a gliding bass, and quiet drips, through a tape echo and a plate reverb. You don't perform it. You tend it. Pick a piece, choose a scale, take notes out, put them back, and leave the pond to grow.

POND is derived from [AMB-1](https://github.com/charlesvestal/fm1-amb) by Charles Vestal. The package identity is `FM-1_8…`, so it does not collide with AMB-1, and a saved AMB-1 project is not read as a pond.

## The screen

The picture is a pond seen from the bank. Flower heads shift a little in the wind. Now and then a koi rises, crosses the open water, and sinks again. The header keeps the piece, the key, and the tempo. The knob strip slides away after three seconds, and the pond continues into that space. Turn a knob, or change page, and the strip comes back.

Rain falls as streaks and lands in rings that spread and fade. The water sits under cloud. Thunder is darker. Lightning flashes, sometimes with a bolt and sometimes only as light, and it does not always arrive with the sound. Freeze the pond and the corner reads "still".

## Pieces

PRESETS steps through the nine pieces. ALGO is the scale.

| Piece | Character |
| --- | --- |
| Pond | The garden at rest. D Dorian. |
| Lily | Few drips, drops an octave down. E major pentatonic. |
| Reeds | Voices, and almost no drops or drips. F Aeolian. |
| Dragonfly | Brighter, quicker, more splash. G Lydian. |
| Evening | A lower bass, slower. A Aeolian. |
| Rain | Heavier drops and drips. The pond is overcast. C Dorian. |
| Moss | Warm, and a little lower. B flat Mixolydian. |
| Still | Slow, with more drift. D Dorian. |
| Thunder | The pad and the drops stay quiet. Rain, a long bass roll, and lightning. C Dorian. |

## Controls

| | |
| --- | --- |
| Keys | The scale. A key adds its note or takes it out. |
| PLAY · REC · EDIT | Grow or rest · freeze · the next chord, on the next bar |
| HOME · ENV · ARP · LFO · SEQ · FX · GLO | Pond, Pad, Drops, Depth, Drips, Still, Setup |
| PRESETS | The piece |
| ALGO | The scale |
| SAVE, held | Saves all nine pieces. Keep holding and the piece returns to its recipe. |

## Try it in the browser

The firmware emulator is the same screen and the same engine as the device. It needs [Emscripten](https://emscripten.org/) and the `base/` checkout.

```
git clone --recursive git@github.com:superxor/amb-pond.git
cd amb-pond
./build.sh --web
python3 -m http.server -d app/build/emu --bind 127.0.0.1 8766
```

Open <http://127.0.0.1:8766/> and press Switch on.

`web/app` is a separate page that runs the engine on its own, for a phone or a desktop browser:

```
sh web/app/build.sh
python3 -m http.server -d app/build/app --bind 127.0.0.1 8765
```

Open <http://127.0.0.1:8765/> and press Begin.

## On the FM-1

`./build.sh` writes `app/build/pond.fwsc`. The toolchain, the tests, and installing from the command line are in [BUILDING.md](BUILDING.md). Installing firmware is at your own risk.

## Credits

The generative plan, the plate, and the Euclidean rhythms come from AMB-1 by Charles Vestal (MPL-2.0): Brian Eno's unequal tape loops, Jon Dattorro's plate by way of FoMni, and Godfried Toussaint's reading of Bjorklund. The platform is [fm1-base](https://github.com/charlesvestal/fm1-base) and [felucca-bsp](https://github.com/hugelton/felucca-bsp), from Felucca by Leo Kuroshita (Hügelton Instruments). See [LICENSING.md](LICENSING.md).

M-VAVE and FM-1 are trademarks of their owners. POND is not affiliated with M-VAVE, Brian Eno, or Hügelton Instruments.
