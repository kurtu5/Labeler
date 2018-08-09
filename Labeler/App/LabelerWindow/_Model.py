# Make import work like include(./../pkg)
import os, sys
try:
    file = __file__
except:
    file = sys.argv[0]
suffix = '\\..'
path=os.path.dirname(os.path.abspath(__file__)) + suffix
sys.path.insert(0, path)

import MVPBase


class Model(MVPBase.BaseModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.selected_indexes = set()
        self.image_files = {}  # {index->image_file}

    def start(self, *args, **kwargs):
        super().start(*args, **kwargs)

         # Let guiM know im showable
        self.sib('gui').window_model_showable(self)
        self.max_columns = self.observer.event_gen('max_columns', 2)


    def load_images(self):
        self.sib('images').load_images()
        index = 0
#        print("images model", self.sib('images').image_files)
        for image_file in self.sib('images').image_files:
#            print("-------------image_file", index, image_file)
            self.image_files[index] = image_file
            index += 1

    def image_select(self, index):
        if index not in self.selected_indexes:
            self.selected_indexes.add(index)

    def image_deselect(self, index):
        if index in self.selected_indexes:
            self.selected_indexes.remove(index)

    def get_all_images(self):
        return self.image_files

    def get_selected_images(self):
        selected_images = {}
        for selected_index in self.selected_indexes:
            for index, image_file in self.image_files.items():
                if selected_index == index:
                    selected_images[index] = image_file
        return selected_images

    # Probably don't need these.  USe the listWidget select to page through images
    def image_select_next(self):
        selected = self.selected_indexes
        if selected == {}:
            index = 1
        else:
            last = list(selected)[-1]
            index = last + 1 if last < len(self.image_files) -1 else 0
        self.image_select(index)

    def image_select_prev(self):
        selected = self.selected_indexes
        if selected == {}:
            index=len(self.image_files) - 1
        else:
            first = list(selected)[-1]
            index = first - 1 if first > 0 else len(self.image_files) - 1
        self.image_select(index)

#    def get_image(self):
#        self.image_file = self.sib('images').image_file
#        self.image_index = self.sib('images').image_index
#
#    def get_images(self):
#        images = []
#        for image in self.sib('images').images:
#            images.append(self.sib('images').path + "\\" + image)
#        return images
#
#    def indexed_image(self, index):
#        self.sib('images').indexed(index)
#        self.get_image()
#
#    def next_image(self):
#        self.sib('images').next()
#        self.get_image()
#
#    def prev_image(self):
#        self.sib('images').prev()
#        self.get_image()

    def status_text_update(self, text):
        self.sib('gui').status_text.set(text)
