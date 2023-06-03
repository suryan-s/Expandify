import os
import asyncio
import pynecone as pc
from typing import List


class State(pc.State):
    """The app state."""
    files_path: str = f".web/public/files/"
    str_files: str = ""
    is_uploading: bool = False

    async def handle_upload(self, files: List[pc.UploadFile]):
        self.is_uploading = True
        if False is os.path.exists(self.files_path):
            os.makedirs(self.files_path, 0o755)
        for file in files:
            upload_data = await file.read()
            output_filepath = self.files_path + file.filename
            with open(output_filepath, "wb") as file_object:
                file_object.write(upload_data)
        return self.show_files

    async def show_files(self):
        await asyncio.sleep(1.0)
        self.is_uploading = False
        if False is os.path.exists(self.files_path):
            os.makedirs(self.files_path, 0o755)
        filelist = os.listdir(self.files_path)
        self.str_files = ""
        for filename in filelist:
            self.str_files = self.str_files + filename + "\n"


color = "rgb(107,99,246)"


def index():
    return pc.vstack()


# Add state and page to the app.
app = pc.App(state=State, on_load=State.show_files)
app.add_page(index, title="Upload")
app.compile()
