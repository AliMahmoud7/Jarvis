import os
import sys
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
# import subprocess
from tempfile import gettempdir
from playsound import playsound
from pygame import mixer
from random import randrange


def tts(message):
    # Create a client using the credentials and region defined in the [adminuser]
    # section of the AWS credentials file (~/.aws/credentials).
    session = Session(
        aws_access_key_id="AKIAJIRJKU4XH2ZDYM2A",
        aws_secret_access_key="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",
        region_name="us-west-2",
    )
    polly = session.client("polly")

    try:
        # Request speech synthesis
        response = polly.synthesize_speech(Text=message, OutputFormat="mp3",
                                           VoiceId="Matthew")
    except (BotoCoreError, ClientError) as error:
        # The service returned an error, exit gracefully
        print(error)
        return tts2(message)
        # sys.exit(-1)

    # Access the audio stream from the response
    if "AudioStream" in response:
        # Note: Closing the stream is important as the service throttles on the
        # number of parallel connections. Here we are using contextlib.closing to
        # ensure the close method of the stream object will be called automatically
        # at the end of the with statement's scope.
        with closing(response["AudioStream"]) as stream:
            output = os.path.join(gettempdir(), "speech{}.mp3".format(randrange(1000)))
            # output = os.path.join(os.getcwd(), "speech{}.mp3".format(randrange(100)))

            try:
                # Open a file for writing the output as a binary stream
                with open(output, "wb") as file:
                    file.write(stream.read())
            except IOError as error:
                # Could not write to file, exit gracefully
                print('IOError in aws tts: ', error)
                sys.exit(-1)
    else:
        # The response didn't contain audio data, exit gracefully
        print("Could not stream audio")
        sys.exit(-1)

    # Play the audio using the platform's default player
    if sys.platform == "win32":
        # print('on windows')
        # mixer.init()
        # mixer.music.load(output)
        # mixer.music.play()
        # while mixer.music.get_busy():
        #     continue
        return playsound(output)
        # os.startfile(output)
    else:
        # the following works on Mac and Linux. (Darwin = mac, xdg-open = linux).
        # opener = "open" if sys.platform == "darwin" else "xdg-open"
        # print([opener, output])
        # subprocess.call([opener, output])
        mixer.init()
        mixer.music.load(output)
        mixer.music.play()
        while mixer.music.get_busy():
            continue
        return None


def tts2(message):
    """
    This function takes a message as an argument and converts it to speech
    depending on the OS.
    """
    if sys.platform == 'darwin':
        tts_engine = 'say'
        return os.system('{} "{}"'.format(tts_engine, message))
    elif sys.platform == 'linux2' or sys.platform == 'linux' or sys.platform == 'win32':
        tts_engine = 'espeak'
        return os.system('{} "{}"'.format(tts_engine, message))
