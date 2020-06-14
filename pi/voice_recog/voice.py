from google.cloud import storage, speech_v1p1beta1
import subprocess
import random
import sys

class VoiceRecog():
    """
    Capture and recognise search phrase using Google Assistant API.
    :param str search_str: the car number recognised result.
    """
    
    def __init__(self):
        self.postfix = random.randint(1000,10000)
        self.file_name = "audio_{}.wav".format(self.postfix)
        self.search_str = ""

    def recog(self):
        print("----------------------------------------")
        print("Start recording, press CTRL+C to finish")
        try:
            process = subprocess.run(
                ["arecord","-f", "S16_LE", "-r", "16000","-t", "wav", self.file_name])
        except KeyboardInterrupt:
            print("Speech recorded, processing for voice recognition.")

        bucket_name = "search_audio" # "your-bucket-name"
        source_file_name = "./{}".format(self.file_name) # "local/path/to/file"
        destination_blob_name = self.file_name #"storage-object-name"

        client = speech_v1p1beta1.SpeechClient()
        storage_uri = 'gs://search_audio/{}'.format(self.file_name)

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)

        print("......")

        # The language of the supplied audio
        language_code = "en-AU"

        config = {
            "language_code": language_code,
        }
        audio = {"uri": storage_uri}

        response = client.recognize(config, audio)
        # print(response)

        for result in response.results:
            # First alternative is the most probable result
            alternative = result.alternatives[0]
            print(u"You spoke: {}".format(alternative.transcript))
            words = alternative.transcript
            word_list = words.split()
            if(len(word_list)==3 and word_list[0] == "car"):
                self.search_str = word_list[2]
            else:
                print("Your speech didn't match the search format, please try again.")
            break