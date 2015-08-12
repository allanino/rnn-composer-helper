# RNN composer help

Here I share some scripts I used to help me on training [char-rnn](https://github.com/karpathy/char-rnn)
to learn to compose tunes in [ABC notation](abcnotation.com).

I keep a blog called [RNN music of the day](http://allanino.me/rnn-music-of-the-day/)
where each day I posted one tune generated by this method.

I don't share my dataset as I'm not sure about possible copyright issues.

## Pre-requisites

You'll need to install Torch and the other requirements from [char-rnn](https://github.com/karpathy/char-rnn).
Just follow the instructions.

I rely heavily on system calls to get the job done, so you'll need to install
some tools on your machine for these scripts to work:

- [abcm2ps](https://github.com/leesavide/abcm2ps)
- [midi2abc](https://github.com/torotil/abcmidi)
- [fluidsynth](http://www.fluidsynth.org/)
- [avconv](https://libav.org/avconv.html)

Some python modules that can be installed by:

```
pip install beautifulsoup4 requests
```

Beautiful Soup is used by a crawler I wrote to get some more data.

We also need a dataset (obviously) and some soundfounts to convert the generated
music to MP3.

Let's see we can get files to train the network.

## Getting files to train the network

I searched the web with preference to huge ABC collecions. The most important files
I found are these:

- [Combined_Tunebook.abc](https://github.com/rjl20/abc-tunebook/blob/master/Combined_Tunebook.abc)
- [HAN1.abc](http://ifdo.ca/~seymour/runabc/esac/HAN1.abc) and [HAN2.abc](http://ifdo.ca/~seymour/runabc/esac/HAN2.abc) (Chinese tunes)
- [nyfte.abc](http://trillian.mit.edu/~jc/music/abc/mirror/nyfte.freezope.org/nyfte.abc)
- All collections from [http://www.lesession.co.uk/music/](http://www.lesession.co.uk/music/)
- All collections from [http://www.norbeck.nu/abc/](http://www.norbeck.nu/abc/)
- All collections from [http://abc.sourceforge.net/NMD/](http://abc.sourceforge.net/NMD/)
- The entire Hanny Christen collection from [https://www.dropbox.com/sh/flddgymslo57zvl/AAAz5s386GT0d4amGpHb8wDXa](https://www.dropbox.com/sh/flddgymslo57zvl/AAAz5s386GT0d4amGpHb8wDXa)
- Some random books from [http://www.campin.me.uk/](http://www.campin.me.uk/)
- Some random collections from [http://www.cranfordpub.com/tunes/abcs/abc_tunes.htm](http://www.cranfordpub.com/tunes/abcs/abc_tunes.htm)
- Most files with than 50 tunes from [http://www.paulhardy.net/](http://www.paulhardy.net/)
- Books 1 to 46 from [http://trillian.mit.edu/~jc/music/book/SCD/](http://trillian.mit.edu/~jc/music/book/SCD/)
- Tunes from a Dropbox user: use the `get_u_4496965_data.py` script. These are some
nice tunes from


From the above links, I must emphasize the Hanny Christen collection of Swiss
folk music for two reasons: it's huge with over 10000 tunes (about 4.4 MB after I
preprocessed it) and all it's musics have chords, giving rise to richer compositions.
I have indeed trained the network on this data alone and got great results.

If I forgot something, please open an issue and I'll update this.

## My workflow

I'll just give an overview here. Each script has some helper, just pass the flag
`-h` to them.

1. Use `preprocess.py` to concatenate and shuffle all files into one big file.
2. Train [char-rnn](https://github.com/karpathy/char-rnn) on that file.
3. Sample trained network to generate a big file with compositons (using `seqlen=100000` tipically).
4. Use `file_to_midi_and_abc.py` to convert that big file into many MIDI files and ABC files.
5. Use `abc_to_mp3.py` to convert the MIDI files into MP3 files.
6. Use `abc_to_svg.py` to convert the ABC files into SVG sheets.

Step 5 needs one more clarification: I used sounfount [754-Donnys Guitar](ftp://93.81.12.10/Soft/Music%20Soft/Samples/Soundfonts/Guitars%20&%20so%20on/Acoustic/754-Donnys%20Guitar.SF2)
to synthesize better sounding files.

## Tips on training `char-rnn`

Be careful to not overfit. Specially when using small datasets. One time I found
marvelous results on a 200 KB dataset just to discover that some tunes were plagiarism
of the training set. One of the indications of overfitting is to have evaluation loss
much larger than training loss. In that case, you should use less memory units or get
a larger dataset.
