import subprocess
import re
import uuid

EPISODE_INTEGRATED_LOUDNESS_RANGE = (-13.5, -15.5)


class AudioHelper(object):

    @staticmethod
    def execute_ffmpeg_command(command_filter):
        output = subprocess.getoutput("ffmpeg {command_filter}".format(**{
            'command_filter': command_filter,
        }))
        return output

    @staticmethod
    def get_audio_loudness_information(audio_file_path):
        """
        Get volume information from an audio file using FFmpeg.
        :param audio_file_path:
        :return:
        """
        # Run FFmpeg command to get 'loudnorm' filter output
        output = AudioHelper.execute_ffmpeg_command(
            "-i {audio_file} -af loudnorm=print_format=summary -f null /dev/null".format(
                **{
                    'audio_file': audio_file_path,
                })
        )

        # Define regular expressions to extract information
        # Input Loudness Patterns
        input_integrated_pattern = r'Input Integrated:\s+([-+]?\d+\.\d+|[-+]inf)\s+LUFS'
        input_true_peak_pattern = r'Input True Peak:\s+([-+]?\d+\.\d+|[-+]inf)\s+dBTP'
        input_lra_pattern = r'Input LRA:\s+([-+]?\d+\.\d+)\s+LU'
        input_threshold_pattern = r'Input Threshold:\s+([-+]?\d+\.\d+|[-+]inf)\s+LUFS'

        # Output Loudness Patterns
        output_integrated_pattern = r'Output Integrated:\s+([-+]?\d+\.\d+|[-+]inf)\s+LUFS'
        output_true_peak_pattern = r'Output True Peak:\s+([-+]?\d+\.\d+|[-+]inf)\s+dBTP'
        output_lra_pattern = r'Output LRA:\s+([-+]?\d+\.\d+)\s+LU'
        output_threshold_pattern = r'Output Threshold:\s+([-+]?\d+\.\d+|[-+]inf)\s+LUFS'

        # Normalization Type and Target Offset Patterns
        normalization_type_pattern = r'Normalization Type:\s+(.+)'
        target_offset_pattern = r'Target Offset:\s+([-+]?\d+\.\d+|[-+]inf)\s+LU'

        # Extract information using regular expressions
        input_integrated = re.search(input_integrated_pattern, output)
        input_true_peak = re.search(input_true_peak_pattern, output)
        input_lra = re.search(input_lra_pattern, output)
        input_threshold = re.search(input_threshold_pattern, output)
        output_integrated = re.search(output_integrated_pattern, output)
        output_true_peak = re.search(output_true_peak_pattern, output)
        output_lra = re.search(output_lra_pattern, output)
        output_threshold = re.search(output_threshold_pattern, output)
        normalization_type = re.search(normalization_type_pattern, output)
        target_offset = re.search(target_offset_pattern, output)

        # Store extracted information in a dictionary
        loudness_info = {
            "input_integrated": input_integrated.group(1),
            "input_true_peak": input_true_peak.group(1),
            "input_lra": input_lra.group(1),
            "input_threshold": input_threshold.group(1),
            "output_integrated": output_integrated.group(1),
            "output_true_peak": output_true_peak.group(1),
            "output_lra": output_lra.group(1),
            "output_threshold": output_threshold.group(1),
            "normalization_type": normalization_type.group(1),
            "target_offset": target_offset.group(1)
        }

        # Store the extracted information in variables
        return loudness_info

    @staticmethod
    def normalize_audio_loudness(input_path, output_path, input_integrated, input_true_peak, input_lra, input_threshold,
                                 offset, linear=True, print_format='summary'):
        """
        Get volume information from an audio file using FFmpeg.
        :param print_format:
        :param offset:
        :param linear:
        :param input_path:
        :param output_path:
        :param input_integrated:
        :param input_true_peak:
        :param input_lra:
        :param input_threshold:
        :return:
        """
        # Run FFmpeg command to get 'loudnorm' filter output

        command_filter = f"-i {input_path} -af loudnorm=I=-14:TP=-1.5:LRA=11:"
        command_filter += f"measured_I={input_integrated}:"
        command_filter += f"measured_TP={input_true_peak}:"
        command_filter += f"measured_LRA={input_lra}:"
        command_filter += f"measured_thresh={input_threshold}:"
        command_filter += f"offset={offset}:"
        command_filter += f"linear={str(linear).lower()}:"
        command_filter += f"print_format={print_format}:"
        command_filter += f" {output_path}"

        output = AudioHelper.execute_ffmpeg_command(command_filter=command_filter)

        # Define regular expressions to extract information
        input_integrated_pattern = r'Input Integrated:\s+(-?\d+\.\d+)\s+LUFS'
        input_true_peak_pattern = r'Input True Peak:\s+([-+]?\d+\.\d+)\s+dBTP'
        input_lra_pattern = r'Input LRA:\s+(-?\d+\.\d+)\s+LU'
        input_threshold_pattern = r'Input Threshold:\s+(-?\d+\.\d+)\s+LUFS'
        output_integrated_pattern = r'Output Integrated:\s+(-?\d+\.\d+)\s+LUFS'
        output_true_peak_pattern = r'Output True Peak:\s+(-?\d+\.\d+)\s+dBTP'
        output_lra_pattern = r'Output LRA:\s+(-?\d+\.\d+)\s+LU'
        output_threshold_pattern = r'Output Threshold:\s+(-?\d+\.\d+)\s+LUFS'
        normalization_type_pattern = r'Normalization Type:\s+(.+)'
        target_offset_pattern = r'Target Offset:\s+([-+]\d+\.\d+)\s+LU'

        # Extract information using regular expressions
        input_integrated = re.search(input_integrated_pattern, output)
        input_true_peak = re.search(input_true_peak_pattern, output)
        input_lra = re.search(input_lra_pattern, output)
        input_threshold = re.search(input_threshold_pattern, output)
        output_integrated = re.search(output_integrated_pattern, output)
        output_true_peak = re.search(output_true_peak_pattern, output)
        output_lra = re.search(output_lra_pattern, output)
        output_threshold = re.search(output_threshold_pattern, output)
        normalization_type = re.search(normalization_type_pattern, output)
        target_offset = re.search(target_offset_pattern, output)

        # Store extracted information in a dictionary
        loudness_info = {
            "input_integrated": input_integrated.group(1),
            "input_true_peak": input_true_peak.group(1),
            "input_lra": input_lra.group(1),
            "input_threshold": input_threshold.group(1),
            "output_integrated": output_integrated.group(1),
            "output_true_peak": output_true_peak.group(1),
            "output_lra": output_lra.group(1),
            "output_threshold": output_threshold.group(1),
            "normalization_type": normalization_type.group(1),
            "target_offset": target_offset.group(1)
        }

        # Store the extracted information in variables
        return loudness_info

    @staticmethod
    def is_audio_normalized(input_integrated) -> bool:
        if not input_integrated:
            return False
        return bool(
            # `EPISODE_INTEGRATED_LOUDNESS_RANGE[0]` is the minimum integrated loudness value.
            EPISODE_INTEGRATED_LOUDNESS_RANGE[0] >=
            # In case of an error, we do not perform loudness normalization;
            float(input_integrated)
            # `EPISODE_INTEGRATED_LOUDNESS_RANGE[1]` is the maximum integrated loudness value.
            >= EPISODE_INTEGRATED_LOUDNESS_RANGE[1]
        )


    @staticmethod
    def normalize_audio(audio_file_path):
        """Normalize audio loudness for an episode"""

        EPISODE_INTEGRATED_LOUDNESS_RANGE = (-13.5, -15.5)
        # Get the audio file, download it, and prepare for loudness analysis
        extension = audio_file_path.split('.')[-1]
        output_path = 'output_audio_{}.{}'.format(str(uuid.uuid4())[:4],extension)

        try:
            # Calculate audio loudness information
            audio_loudness_output = AudioHelper.get_audio_loudness_information(audio_file_path=audio_file_path)
            print("looudness get")
            is_eligible_for_normalization = not bool(
                EPISODE_INTEGRATED_LOUDNESS_RANGE[0] >= float(audio_loudness_output.get('input_integrated')) >=
                EPISODE_INTEGRATED_LOUDNESS_RANGE[1]
            )

            # Normalize audio loudness
            normalized_data = AudioHelper.normalize_audio_loudness(
                    input_path=audio_file_path,
                    output_path=output_path,
                    input_integrated=audio_loudness_output.get('input_integrated'),
                    input_true_peak=audio_loudness_output.get('input_true_peak'),
                    input_lra=audio_loudness_output.get('input_lra'),
                    input_threshold=audio_loudness_output.get('input_threshold'),
                    offset=audio_loudness_output.get('target_offset'),
                )
            print("normalized")


        except Exception as e:
            print(e)

