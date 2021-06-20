from mathutils import Vector


class NameFix:
    def __init__(self, armature):
        self.threshold = 0.01
        self.armature = armature

        self.right_bones = []
        self.left_bones = []
        self.mid_bones = []

        self.collect_left_right()

    def collect_left_right(self):
        self.right_bones.clear()
        self.left_bones.clear()

        for bone in self.armature.data.bones:
            if bone.name.endswith(('.R', '.L')):
                continue
            if abs(bone.head_local.x) < self.threshold:
                if abs(bone.tail_local.x) < self.threshold:
                    self.mid_bones.append(bone.name)
                    continue
                elif bone.tail_local.x < 0:
                    self.right_bones.append(bone.name)
                    continue
                else:
                    self.left_bones.append(bone.name)
                    continue

            if bone.head_local.x < 0:
                self.right_bones.append(bone.name)
            else:
                self.left_bones.append(bone.name)

    def names_to_bones(self, names):
        self.armature.update_from_editmode()
        for name in names:
            yield self.armature.data.bones[name]

    def name_left_right(self):
        threshold = 0.01

        new_names = dict()

        for lbone in self.names_to_bones(self.left_bones):
            if lbone.name.endswith(('.L', '.R')):
                continue

            new_names[lbone.name] = lbone.name + ".L"

            right_loc = lbone.head_local.copy()
            right_loc.x = -right_loc.x

            for rbone in self.names_to_bones(self.right_bones):
                match = True
                for i in range(3):
                    if abs(rbone.head_local[i] - right_loc[i]) > threshold:
                        match = False
                        break
                if match:
                    new_names[rbone.name] = lbone.name + ".R"

        for k, v in new_names.items():
            self.armature.data.bones[k].name = v

        self.left_bones = [new_names.get(name, name) for name in self.left_bones]
        self.right_bones = [new_names.get(name, name) for name in self.right_bones]

    def fix(self):
        self.name_left_right()
