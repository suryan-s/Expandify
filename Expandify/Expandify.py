import glob
import os
import asyncio
import shutil

import pynecone as pc
import zipfile
import uuid
from typing import List



class State(pc.State):
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

    images_train: int = 0
    images_test: int = 0
    images_valid: int = 0

    annot_train: int = 0
    annot_test: int = 0
    annot_valid: int = 0

    operations = [
        'Flip',
        'Rotation', 'Shear',
        'Grayscale', 'Hue',
        'Saturation', 'Brightness',
        'Exposure', 'Blur'
    ]

    is_flip: bool = False
    is_rotate: bool = False
    is_shear: bool = False
    is_gray: bool = False
    is_hue: bool = False
    is_satur: bool = False
    is_bright: bool = False
    is_expos: bool = False
    is_blur: bool = False

    final_loc_image: str = ""
    final_loc_label: str = ""
    
    start : bool = False
    ready : bool = False

    def want_flip(self):
        # self.is_flip = not self.is_flip
        pass

    def want_rotate(self):
        # self.is_rotate = not self.is_rotate
        pass

    def want_shear(self):
        # self.is_shear = not self.is_shear
        pass

    def want_gray(self):
        # self.is_gray = not self.is_gray
        pass

    def want_hue(self):
        # self.is_hue = not self.is_hue
        pass

    def want_satur(self):
        # self.is_satur = not self.is_satur
        pass

    def want_bright(self):
        # self.is_bright = not self.is_bright
        pass

    def want_expos(self):
        # self.is_expos = not self.is_expos
        pass

    def want_blur(self):
        # self.is_blur = not self.is_blur
        pass
    
    def start_aug(self):
        self.start = True
        
    def ready_aug(self):
        self.ready = True
    
    # @pc.var
    async def augmentation(self):
        image_list = os.listdir(self.final_loc_image)
        label_list = os.listdir(self.final_loc_label)
        print(image_list)
        print(label_list)
        print("done")
        pass


    async def handle_upload(self, files: List[pc.UploadFile]):
        self.is_uploading = True
        self.is_file_available = False
        self.new_files_path = self.files_path + f"{uuid.uuid4()}/"
        if not os.path.exists(self.new_files_path):
            os.makedirs(self.new_files_path, 0o755)
            os.makedirs(self.new_files_path + "operations", 0o755)
            os.makedirs(self.new_files_path + "operations/" + "images", 0o755)
            os.makedirs(self.new_files_path + "operations/" + "labels", 0o755)
            os.makedirs(self.new_files_path + "extracted", 0o755)
            os.makedirs(self.new_files_path + "download", 0o755)
        for file in files:
            upload_data = await file.read()
            print("Save zipfile")
            self.str_files = f"{file.filename}"
            output_filepath = self.new_files_path + file.filename # type: ignore
            with open(output_filepath, "wb") as file_object:
                file_object.write(upload_data)
            with zipfile.ZipFile(output_filepath, "r") as zipf:
                zipf.extractall(self.new_files_path + "extracted")
            print("Done unzipping")
            self.is_uploading = False
            self.is_file_available = True
        return await self.show_files(self.new_files_path + "extracted")

    async def move_files(self, source_path: str, destination_path: str):
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)

        files = os.listdir(source_path)
        for file in files:
            source_file = os.path.join(source_path, file)
            destination_file = os.path.join(destination_path, file)
            shutil.move(source_file, destination_file)

    async def show_files(self, fpath: str):
        # await asyncio.sleep(1.0)
        # self.is_file_available = True
        folder_name = os.listdir(fpath)[0]

        train_dir = os.path.join(fpath, folder_name, 'train')
        test_dir = os.path.join(fpath, folder_name, 'test')
        valid_dir = os.path.join(fpath, folder_name, 'valid')

        if os.path.exists(train_dir):
            self.images_train = len(glob.glob(os.path.join(train_dir, 'images', '*')))
            self.annot_train = len(glob.glob(os.path.join(train_dir, 'labels', '*')))

        if os.path.exists(test_dir):
            self.images_test = len(glob.glob(os.path.join(test_dir, 'images', '*')))
            self.annot_test = len(glob.glob(os.path.join(test_dir, 'labels', '*')))

        if os.path.exists(valid_dir):
            self.images_valid = len(glob.glob(os.path.join(valid_dir, 'images', '*')))
            self.annot_valid = len(glob.glob(os.path.join(valid_dir, 'labels', '*')))
        await self.preprocess(fpath, folder_name)

    async def preprocess(self, fpath: str, folder_name: str):
        spath = fpath.replace('extracted', 'operations')

        for data_type in ['train', 'test', 'valid']:
            data_path = os.path.join(fpath, folder_name, data_type)
            if os.path.exists(data_path):
                image_path = os.path.join(data_path, 'images')
                label_path = os.path.join(data_path, 'labels')
                destination_image_path = os.path.join(spath, 'images')
                destination_label_path = os.path.join(spath, 'labels')

                if os.path.exists(image_path):
                    await self.move_files(image_path, destination_image_path)

                if os.path.exists(label_path):
                    await self.move_files(label_path, destination_label_path)
                self.final_loc_image = destination_image_path
                self.final_loc_label = destination_label_path
            # while( self.start == False):
            #     await asyncio.sleep(1.0)
            # await self.augmentation()    


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
                                            pc.text(
                                                "Great! Your zip file has been finished processing. Move to view tab "
                                                "to view your files"
                                            ),
                                            pc.button(
                                                "Upload",
                                                on_click=State.handle_upload(pc.upload_files()), # type: ignore
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
                            # View items
                            pc.tab_panel(
                                pc.cond(
                                    State.is_file_available,
                                    pc.vstack(
                                        pc.spacer(),
                                        pc.text("This is the structure of your uploaded data", font_size="1.25rem"),
                                        pc.spacer(),
                                        pc.spacer(),
                                        pc.table_container(
                                            pc.table(
                                                headers=["Directory", "Images", "Annotations"],
                                                rows=[
                                                    ("Train", State.images_train, State.annot_train),
                                                    ("Test", State.images_test, State.annot_test),
                                                    ("Validation", State.images_valid, State.annot_valid),
                                                ],
                                                variant="striped",
                                            ),
                                            pc.spacer(),
                                            pc.spacer(),
                                            pc.text(
                                                "Continue to generate tab to start augmenting and transforming your "
                                                "sample dataset to create new training samples ",
                                                padding="50px"
                                            ),
                                            padding="50px"
                                        ),
                                    ),
                                    pc.center(
                                        pc.text("No sample dataset provided", font_size="1.25rem")
                                    )
                                ),
                                panel_id="#2",
                                is_lazy=True
                            ),
                            # Generate
                            pc.tab_panel(
                                pc.cond(
                                    State.is_file_available,
                                    pc.vstack(
                                        pc.spacer(),
                                        pc.text("Start augmenting for sample dataset", font_size="1.25rem"),
                                        pc.spacer(),
                                        pc.accordion(
                                            pc.accordion_item(
                                                pc.accordion_button(
                                                    pc.text("Rotate"),
                                                    pc.accordion_icon(),
                                                ),
                                                pc.accordion_panel(
                                                    pc.hstack(
                                                        pc.text(
                                                            "Rotate image Between -10° and +10°."
                                                        ),
                                                        pc.spacer(),
                                                        pc.checkbox(
                                                            "Rotate",
                                                            color_scheme="green",
                                                            size="lg",
                                                            # on_change=State.want_rotate
                                                        ),
                                                    )
                                                ),
                                            ),
                                            pc.accordion_item(
                                                pc.accordion_button(
                                                    pc.text("Flip"),
                                                    pc.accordion_icon(),
                                                ),
                                                pc.accordion_panel(
                                                    pc.hstack(
                                                        pc.text(
                                                            "Flip image horizontally."
                                                        ),
                                                        pc.spacer(),
                                                        pc.checkbox(
                                                            "Flip",
                                                            color_scheme="green",
                                                            size="lg",
                                                            # on_change=State.want_flip
                                                        ),
                                                    )
                                                ),
                                            ),
                                            pc.accordion_item(
                                                pc.accordion_button(
                                                    pc.text("Shear"),
                                                    pc.accordion_icon(),
                                                ),
                                                pc.accordion_panel(
                                                    pc.hstack(
                                                        pc.text(
                                                            "Shear image ±2° Horizontal, ±2° Vertical."
                                                        ),
                                                        pc.spacer(),
                                                        pc.checkbox(
                                                            "Shear",
                                                            color_scheme="green",
                                                            size="lg",
                                                            # on_change=State.want_shear
                                                        ),
                                                    )
                                                ),
                                            ),
                                            pc.accordion_item(
                                                pc.accordion_button(
                                                    pc.text("Grayscale"),
                                                    pc.accordion_icon(),
                                                ),
                                                pc.accordion_panel(
                                                    pc.hstack(
                                                        pc.text(
                                                            "Grayscale image ±2° Horizontal, ±2° Vertical."
                                                        ),
                                                        pc.spacer(),
                                                        pc.checkbox(
                                                            "Grayscale",
                                                            color_scheme="green",
                                                            size="lg",
                                                            # on_change=State.want_gray
                                                        ),
                                                    )
                                                )
                                            ),
                                            pc.accordion_item(
                                                pc.accordion_button(
                                                    pc.text("Hue"),
                                                    pc.accordion_icon(),
                                                ),
                                                pc.accordion_panel(
                                                    pc.hstack(
                                                        pc.text(
                                                            "Hue image ±2° Horizontal, ±2° Vertical."
                                                        ),
                                                        pc.spacer(),
                                                        pc.checkbox(
                                                            "Hue",
                                                            color_scheme="green",
                                                            size="lg",
                                                            # on_change=State.want_hue
                                                        ),
                                                    )
                                                ),
                                            ),
                                            pc.accordion_item(
                                                pc.accordion_button(
                                                    pc.text("Example 6"),
                                                    pc.accordion_icon(),
                                                ),
                                                pc.accordion_panel(
                                                    pc.hstack(
                                                        pc.text(
                                                            "Saturate image ±2° Horizontal, ±2° Vertical."
                                                        ),
                                                        pc.spacer(),
                                                        pc.checkbox(
                                                            "Saturation",
                                                            color_scheme="green",
                                                            size="lg",
                                                            # on_change=State.want_satur
                                                        ),
                                                    )
                                                )
                                            ),
                                            pc.accordion_item(
                                                pc.accordion_button(
                                                    pc.text("Brightness"),
                                                    pc.accordion_icon(),
                                                ),
                                                pc.accordion_panel(
                                                    pc.hstack(
                                                        pc.text(
                                                            "Brighten image ±2° Horizontal, ±2° Vertical."
                                                        ),
                                                        pc.spacer(),
                                                        pc.checkbox(
                                                            "Brightness",
                                                            color_scheme="green",
                                                            size="lg",
                                                            # on_change=State.want_bright
                                                        ),
                                                    )
                                                )
                                            ),
                                            pc.accordion_item(
                                                pc.accordion_button(
                                                    pc.text("Exposure"),
                                                    pc.accordion_icon(),
                                                ),
                                                pc.accordion_panel(
                                                    pc.hstack(
                                                        pc.text(
                                                            "Exposure variation image ±2° Horizontal, ±2° Vertical."
                                                        ),
                                                        pc.spacer(),
                                                        pc.checkbox(
                                                            "Exposure",
                                                            color_scheme="green",
                                                            size="lg",
                                                            # on_change=State.want_expos
                                                        ),
                                                    )
                                                )
                                            ),
                                            pc.accordion_item(
                                                pc.accordion_button(
                                                    pc.text("Blur"),
                                                    pc.accordion_icon(),
                                                ),
                                                pc.accordion_panel(
                                                    pc.hstack(
                                                        pc.text(
                                                            "Blur image ±2° Horizontal, ±2° Vertical."
                                                        ),
                                                        pc.spacer(),
                                                        pc.checkbox(
                                                            "Blur",
                                                            color_scheme="green",
                                                            size="lg",
                                                            # on_change=State.want_blur
                                                        ),
                                                    )
                                                )
                                            ),
                                            width="50%",
                                            allow_multiple=False,
                                            overflow="auto"
                                        ),
                                        pc.spacer(),
                                        pc.button(
                                            "Start",
                                            on_click=State.start_aug,
                                            shadow="lg",
                                        ),
                                        pc.spacer(),
                                        pc.cond(
                                            State.ready,
                                            pc.text("Augmentation is done!"),
                                            pc.circular_progress(
                                                is_indeterminate=True,
                                            )
                                        )

                                    ),
                                    pc.center(
                                        pc.text("No sample dataset provided", font_size="1.25rem")
                                    ),
                                ),
                                panel_id="#3",
                                overflow="auto"
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
            # width="100%"
        ),
        padding="50px",
        width="100%"
    )


# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index, title="Expandify")
app.compile()
