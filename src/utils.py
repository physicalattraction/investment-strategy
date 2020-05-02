import filecmp
import os.path
import shutil
from unittest import TestCase

import settings


class FileComparingMixin(TestCase):
    data_dir = settings.TEST_DIR  # Can be overwritter by concrete implementations

    def compare_file_with_file(self, input_filepath: str, reference_filename: str, name: str = 'file',
                               write_first: bool = False) -> None:
        """
        Compare the input file with a reference file

        :param input_filepath: Full path to the input file to check
        :param reference_filename: File name of the reference file. It is assumed this file exists in self.data_dir
        :param name: Name of the file to check, used in logging
        :param write_first: Flag to indicate whether we first need to write the reference file
        """

        reference_filepath = os.path.join(self.data_dir, reference_filename)
        if write_first:
            shutil.copyfile(input_filepath, dst=reference_filepath)

        if not filecmp.cmp(input_filepath, reference_filepath):
            generated_filename = f'{reference_filename}_generated'
            generated_filepath = os.path.join(self.data_dir, generated_filename)
            shutil.copyfile(src=input_filepath, dst=generated_filepath)
            msg = f'Generated {name} written to: {generated_filename}'
            self.fail(msg)
