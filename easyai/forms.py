import os
from django import forms


class UploadFileForm(forms.Form):
    VALID_EXTENSIONS = ['.csv']
    file = forms.FileField(label="")

    def clean_file(self):
        file = self.cleaned_data['file']
        extension = os.path.splitext(file.name)[1]
        if not extension.lower() in UploadFileForm.VALID_EXTENSIONS:
            raise forms.ValidationError('csvファイルを選択してください')


# TODO: DBから取得
class EasyTargetSettingForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# TODO: DBから取得
class NormalTargetSettingForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['model_type'].widget.attrs['class'] = 'm-1 border-gray-800 focus:outline-none border-none p-2 rounded-md border-r border-gray-300'

    model_type = forms.ChoiceField(
        choices = (
            ('GBDT', 'GBDT'),
            ('NN', 'ニューラルネットワーク'),
            ('RF', 'ランダムフォレスト'),
        ),
        label='モデルの種類を選択してください',
    )


class DeleteStringForm(forms.Form):
    """
    動的に作成するform
    呼び出し元のDeleteStringViewにて定義
    """
    pass


class ReplaceStringForm(forms.Form):
    """
    動的に作成するform
    呼び出し元のReplaceStringViewにて動的生成
    """

class MissingProcessForm(forms.Form):
    """
    動的に作成するform
    呼び出し元のMissingProcessViewにて定義
    """
    pass

class PredictForm(forms.Form):
    """
    動的に作成するform
    呼び出し元のPredictViewとPredictViewにて定義
    """
    pass

class PredictSettingForm(forms.Form):
    """
    動的に作成するform
    呼び出し元のPredictinSettingViewにて定義
    """
    pass