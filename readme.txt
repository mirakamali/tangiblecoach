Tangible coach design

In docs, you can find the assembly manual and the hardware used
you can also find a video that shows the final prototype of the tangible coach.


in nestore, you can find the code.

After you flash a rasbpian image Stretch on your SD card,

You need to first install the kernel modules for matrix voice ( microphones) https://matrix-io.github.io/matrix-documentation/matrix-voice/device-setup/
and https://matrix-io.github.io/matrix-documentation/matrix-lite/py-reference/alsa-mics/

Once your microphone works well

clone this code
cd nestore/
pip install requirements.txt
cd ..
sh nestorescript.sh