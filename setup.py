#!/usr/bin/env python


try:
    from sugar.activity import bundlebuilder
    bundlebuilder.start()
except ImportError:
    import os
    os.system("find ./ | sed 's,^./,ClicPlayer.activity/,g' > MANIFEST")
    os.system('rm ClicPlayer-1.xo')
    os.chdir('..')
    os.system('zip -r ClicPlayer-1.xo ClicPlayer.activity')
    os.system('mv ClicPlayer-1.xo ./ClicPlayer.activity')
    os.chdir('ClicPlayer.activity')

