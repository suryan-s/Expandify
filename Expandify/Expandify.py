import os
import asyncio
import pynecone as pc
from typing import List


class State(pc.State):
    """The app state."""
    files_path: str = f"temp"
    str_files: str = ""
    is_uploading: bool = False
    is_view: bool = False
    is_generate: bool = False
    is_export: bool = False

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


def index():
    return pc.vstack(
        # Main heading
        pc.text(
            "Expandify",
            background_image="linear-gradient(271.68deg, #EE756A 0.75%, #756AEE 88.52%)",
            background_clip="text",
            font_weight="bold",
            font_size="5em",
        ),
        # Sub heading
        pc.box(
            pc.span(
                "Transform and augment your image datasets with ease",
                font_size="2.5em"
            ),
            # pc.span(
            #     ".",
            #     font_size="2em",
            #     color="yellow"
            # ),
            padding="0px 0px 50px 0px"
        ),

        # Main content
        pc.center(
            pc.hstack(
                pc.vstack(
                    pc.tabs(
                        pc.tab_list(
                            pc.tab("Upload", font_size="1.5rem"),
                            pc.tab("View", font_size="1.5rem"),
                            pc.tab("Generate", font_size="1.5rem"),
                            pc.tab("Export", font_size="1.5rem"),
                        ),
                        pc.tab_panels(
                            pc.tab_panel(
                                pc.spacer(),
                                pc.spacer(),
                                pc.cond(
                                    State.is_uploading,
                                    pc.center(
                                        pc.text("Zip file uploaded", font_size="1.25rem")
                                    ),
                                    pc.center(
                                        pc.vstack(
                                            pc.spacer(),
                                            pc.text("Upload the dataset as zip file", font_size="1.25rem"),
                                            pc.spacer(),
                                            pc.upload(
                                                pc.text(
                                                    "Drag and drop zip file here or click to select zip file"
                                                ),
                                                border="1px dotted rgb(107,99,246)",
                                                padding="10em",
                                            )
                                        ),
                                        display="flex",
                                        justify_content="center",
                                        align_items="center",
                                    )
                                )
                            ),
                            pc.tab_panel(
                                pc.text("Text from tab 1.")
                            ),
                            pc.tab_panel(
                                pc.checkbox("Text from tab 2.")
                            ),
                            pc.tab_panel(
                                pc.button("Text from tab 3.", color="black")
                            ),
                        ),
                        bg="526D82",
                        color="F5EFE7",
                        shadow="lg",
                        height="600px",
                        width="1000px",
                        align="center",
                        is_fitted=True,
                    ),
                )
            ),
            # border="2px dotted blue",
            border_style="solid",
            border_width="2px",
            border_image="linear-gradient(271.68deg, #EE756A 0.75%, #756AEE 88.52%)",
            border_image_slice="1",
            padding="20px",
        ),
        padding="50px",
        width="100%"
    )


# Add state and page to the app.
app = pc.App(state=State, on_load=State.show_files)
app.add_page(index, title="Expandify")
app.compile()
