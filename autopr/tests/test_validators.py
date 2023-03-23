@@ -5,3 +5,5 @@
@@ -8,2 +8,4 @@
@@ -106,4 +106,5 @@
+
+if __name__ == "__main__":
+    example_board = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
+    display_board(example_board)
"""
tic_tac_toe_nonexistent_whitespace = """diff --git a/tic_tac_toe.py b/tic_tac_toe.py
new file mode 100644
index 0000000..d46de12
--- /dev/null
+++ b/tic_tac_toe.py
@@ -0,0 +1,18 @@
+def display_board(board):
+    for i in range(3):
+        print(" | ".join(board[i * 3:i * 3 + 3]))
+        if i < 2:
+            print("-" * 9)
+

generation_service_file = "\n" * 7 + """
from autopr.models.rail_objects import PullRequestDescription, InitialFileSelectResponse, LookAtFilesResponse, \\
    Diff, CommitPlan
from autopr.models.rails import InitialFileSelectRail, ContinueLookingAtFiles, LookAtFiles, ProposePullRequest, \\
    NewDiff, FileDescriptor
from autopr.models.repo import RepoCommit
from autopr.models.repo import RepoPullRequest
from autopr.services.rail_service import RailService

import structlog
log = structlog.get_logger()""" + "\n" * 8 + """    ):
        self.rail_service = rail_service
        self.file_context_token_limit = file_context_token_limit
        self.file_chunk_size = file_chunk_size
        self.tokenizer = transformers.GPT2TokenizerFast.from_pretrained('gpt2', model_max_length=8192)

    @staticmethod
    def repo_to_codebase(""" + "\n" * 33 + """
        return filenames_and_contents

    def _repo_to_files_and_token_lengths(
        self,"""
incorrect_generation_service_diff = """--- autopr/services/generation_service.py
+++ autopr/services/generation_service.py
@@ -11,6 +11,7 @@
 from autopr.models.rails import InitialFileSelectRail, ContinueLookingAtFiles, LookAtFiles, ProposePullRequest,     NewDiff, FileDescriptor
 from autopr.models.repo import RepoCommit
 from autopr.models.repo import RepoPullRequest
+from pathlib import Path
 from autopr.services.rail_service import RailService

 import structlog
@@ -28,6 +29,7 @@
         self.file_context_token_limit = file_context_token_limit
         self.file_chunk_size = file_chunk_size
         self.tokenizer = transformers.GPT2TokenizerFast.from_pretrained('gpt2', model_max_length=8192)
+        self.create_gptignore()

     @staticmethod
     def repo_to_codebase(
@@ -67,6 +69,14 @@
         return filenames_and_contents

     def _repo_to_files_and_token_lengths(
+        self,
+        repo_tree: git.Repo,
+        excluded_files: list[str] = None,
+    ) -> list[tuple[str, int]]:
+        files_with_token_lengths = []
+        for blob in repo_tree.traverse():
+            if blob.type == 'tree':
+                continue
+            if excluded_files is not None and blob.path in excluded_files:
+                continue
+            content = blob.data_stream.read().decode()
+            token_length = len(self.rail_service.tokenizer.encode(content))
+            files_with_token_lengths.append((blob.path, token_length))
+        return files_with_token_lengths
+    
+    def create_gptignore(self):
+        gptignore_path = Path('.gptignore')
+        if not gptignore_path.exists():
+            with gptignore_path.open('w') as gptignore_file:
+                gptignore_file.write('*.lock
')"""
correct_generation_service_diff = """--- autopr/autopr/services/generation_service.py
+++ autopr/autopr/services/generation_service.py
@@ -11,0 +11,1 @@
+from pathlib import Path
--- autopr/autopr/services/generation_service.py
+++ autopr/autopr/services/generation_service.py
@@ -28,3 +29,4 @@
         self.file_context_token_limit = file_context_token_limit
         self.file_chunk_size = file_chunk_size
         self.tokenizer = transformers.GPT2TokenizerFast.from_pretrained('gpt2', model_max_length=8192)
+        self.create_gptignore()
--- autopr/autopr/services/generation_service.py
+++ autopr/autopr/services/generation_service.py
@@ -67,3 +69,23 @@
         return filenames_and_contents
 
     def _repo_to_files_and_token_lengths(
+        self,
+        repo_tree: git.Repo,
+        excluded_files: list[str] = None,
+    ) -> list[tuple[str, int]]:
+        files_with_token_lengths = []
+        for blob in repo_tree.traverse():
+            if blob.type == 'tree':
+                continue
+            if excluded_files is not None and blob.path in excluded_files:
+                continue
+            content = blob.data_stream.read().decode()
+            token_length = len(self.rail_service.tokenizer.encode(content))
+            files_with_token_lengths.append((blob.path, token_length))
+        return files_with_token_lengths
+    
+    def create_gptignore(self):
+        gptignore_path = Path('.gptignore')
+        if not gptignore_path.exists():
+            with gptignore_path.open('w') as gptignore_file:
+                gptignore_file.write('*.lock
"""

generation_service_2_file = """import tempfile
from typing import Callable

import git
import pydantic
import transformers
from git import Tree""" + '\n' * 308 + """        repo_tree = repo.head.commit.tree
        files = self._repo_to_file_descriptors(repo_tree)

        # Get the filepaths to look at
        filepaths = self.get_initial_filepaths(files, issue_text)

        if filepaths:"""

generation_service_2_partially_wrong_diff = """--- autopr/services/generation_service.py
+++ autopr/services/generation_service.py
@@ -1,6 +1,7 @@
 import re
 import os
 import tempfile
+import fnmatch
 from typing import List, Dict, Tuple
 from git import Repo, Tree
 from .file_descriptor import FileDescriptor
@@ -315,10 +316,18 @@
     repo_tree = repo.head.commit.tree
     files = self._repo_to_file_descriptors(repo_tree)
 
+    # Load .gptignore patterns
+    with open('.gptignore', 'r') as gptignore_file:
+        ignore_patterns = gptignore_file.read().splitlines()
+
     # Get the filepaths to look at
-    filepaths = self.get_initial_filepaths(files, issue_text)
+    filepaths = [
+        filepath for filepath in self.get_initial_filepaths(files, issue_text)
+        if not any(fnmatch.fnmatch(filepath, pattern) for pattern in ignore_patterns)
+    ]
 
     if filepaths:
         # Look at the files
         notes = self.write_notes_about_files(files, issue_text, filepaths)
"""

generation_service_2_expected_diff = """--- autopr/autopr/services/generation_service.py
+++ autopr/autopr/services/generation_service.py
@@ -1,1 +1,2 @@
 import tempfile
+import fnmatch
--- autopr/autopr/services/generation_service.py
+++ autopr/autopr/services/generation_service.py
@@ -315,5 +316,12 @@
         repo_tree = repo.head.commit.tree
         files = self._repo_to_file_descriptors(repo_tree)
 
+        # Load .gptignore patterns
+        with open('.gptignore', 'r') as gptignore_file:
+            ignore_patterns = gptignore_file.read().splitlines()
+
         # Get the filepaths to look at
-        filepaths = self.get_initial_filepaths(files, issue_text)
+        filepaths = [
+            filepath for filepath in self.get_initial_filepaths(files, issue_text)
+            if not any(fnmatch.fnmatch(filepath, pattern) for pattern in ignore_patterns)
+        ]
"""

                (
                    "Unidiff contains whitespaced lines in new file",
                    tic_tac_toe_nonexistent_whitespace,
                ),
        (
            [
                (
                    "Unidiff contains incorrect filepaths",
                    incorrect_generation_service_diff,
                ),
            ],
            generation_service_file,
            correct_generation_service_diff,
        ),
        (
            [
                (
                    "Unidiff is wrong in first hunk, correct in second hunk",
                    generation_service_2_partially_wrong_diff,
                ),
            ],
            generation_service_2_file,
            generation_service_2_expected_diff,
        ),
        if path in [
            '.gptignore',
            'tic_tac_toe.py',
            '/dev/null'
        ]:
    mock_repo.head.commit.tree.__truediv__.side_effect = truediv_side_effect
    validator_class = create_unidiff_validator(mock_repo)