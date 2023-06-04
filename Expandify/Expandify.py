import os
import asyncio
import pynecone as pc
import zipfile
import uuid
from typing import List


class State(pc.State):
    """The app state."""
    files_path: str = "temp/"
    new_files_path: str = ""
    str_files: str = ""

    is_uploading: bool = False
    is_file_available: bool = False

    isDisable_view: bool = True
    isDisable_generate: bool = True
    isDisable_export: bool = True

    select_upload: bool = True
    select_view: bool = False
    select_generate: bool = False
    select_export: bool = False

    # @pc.memo
    def selected_views(self):
        self.select_view = True
        self.select_upload = False
        self.select_export = False
        self.select_generate = False
        print(f'{self.select_view}, {self.select_upload}, {self.select_generate}, {self.select_export}')

    def selected_generate(self):
        self.select_view = False
        self.select_upload = False
        self.select_export = False
        self.select_generate = True

    def selected_export(self):
        self.select_view = False
        self.select_upload = False
        self.select_export = True
        self.select_generate = False

    async def handle_upload(self, files: List[pc.UploadFile]):
        self.is_uploading = True
        self.is_file_available = False
        self.new_files_path = self.files_path + f"{uuid.uuid4()}/"
        if not os.path.exists(self.new_files_path):
            os.makedirs(self.new_files_path, 0o755)
            os.makedirs(self.new_files_path + "extracted", 0o755)
        for file in files:
            upload_data = await file.read()
            print("Save zipfile")
            self.str_files = f"{file.filename}"
            output_filepath = self.new_files_path + file.filename
            with open(output_filepath, "wb") as file_object:
                file_object.write(upload_data)
            with zipfile.ZipFile(output_filepath, "r") as zipf:
                zipf.extractall(self.new_files_path + "extracted")
            print("Done unzipping")
            self.is_uploading = False
            self.is_file_available = True
        # return self.show_files

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
                            pc.tab(
                                "Upload",
                                font_size="1.5rem",
                                panel_id="#1",
                                # is_selected=False
                            ),
                            pc.tab(
                                "View",
                                font_size="1.5rem",
                                panel_id="#2",
                                # is_disabled=State.isDisable_view,
                                # is_selected=State.select_view
                                # is_selected=True
                            ),
                            pc.tab(
                                "Generate",
                                font_size="1.5rem",
                                panel_id="#3",
                                # is_disabled=State.isDisable_generate,
                                # is_selected=State.select_generate
                            ),
                            pc.tab(
                                "Export",
                                font_size="1.5rem",
                                panel_id="#4",
                                # is_disabled=State.isDisable_export,
                                # is_selected=State.select_export
                            ),
                        ),
                        pc.tab_panels(
                            pc.tab_panel(
                                # Upload
                                pc.spacer(),
                                pc.spacer(),
                                pc.center(
                                    pc.vstack(
                                        pc.spacer(),
                                        pc.text("Upload the dataset as zip file", font_size="1.25rem"),
                                        pc.spacer(),
                                        pc.cond(
                                            State.is_file_available,
                                            pc.text_area(
                                                disabled="True",
                                                default_value='Done uploading : ' + State.str_files,
                                                # width="100%",
                                                # height="100%",
                                                padding="10em",
                                            ),
                                            pc.upload(
                                                pc.text(
                                                    "Drag and drop zip file here or click to select zip file"
                                                ),
                                                border="1px dotted rgb(107,99,246)",
                                                padding="10em",
                                            ),
                                        ),
                                        pc.cond(
                                            State.is_uploading,
                                            pc.progress(is_indeterminate=True, color="EB455F", width="100%"),
                                            pc.progress(value=0, width="100%"),
                                        ),
                                        pc.cond(
                                            State.is_file_available,
                                            # pc.button(
                                            #     "Next",
                                            #     on_click=State.selected_views,
                                            #     position="absolute",
                                            #     bottom="-12",
                                            #     shadow="lg",
                                            # ),
                                            pc.text(
                                                "Great! Your zip file has been finished processing. Move to view tab "
                                                "to view your files"
                                            ),
                                            pc.button(
                                                "Upload",
                                                on_click=State.handle_upload(pc.upload_files()),
                                                position="absolute",
                                                bottom="-12",
                                                shadow="lg",
                                            ),
                                        ),

                                    ),
                                    display="flex",
                                    justify_content="center",
                                    align_items="center",
                                ),
                                panel_id="#1",
                                position="relative",
                            ),
                            pc.tab_panel(
                                pc.text("Text from views."),
                                panel_id="#2"
                            ),
                            pc.tab_panel(
                                pc.text("Text from generate."),
                                panel_id="#3"
                            ),
                            pc.tab_panel(
                                pc.text("Text from export."),
                                panel_id="#4"
                            ),
                        ),
                        bg="526D82",
                        color="F5EFE7",
                        shadow="lg",
                        height="600px",
                        width="1000px",
                        align="center",
                        is_fitted=True,
                        # orientation="vertical"
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
