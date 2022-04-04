from matplotlib.style import use
from easyai.other_modules import SingletonClass
from easyai.abstracts import AbstractModelClass
from easyai.ml_modules import NNClass, GBDTClass, PredictionClass, RFClass

class MLControllClass(SingletonClass):
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__init__()
        return cls._instance

    def __init__(self):
        self.ml_instance = {}
        self.en_instance = {}
        self.predict_instance = {}

    def set_ml_instance(self, user_id, ml_ins):
        self.ml_instance[user_id] = ml_ins

    def get_ml_instance(self, user_id) -> AbstractModelClass:
        return self.ml_instance[user_id]

    def en_instance_init(self, user_id):
        self.en_instance[user_id] = {}

    def set_en_instance(self, user_id, ml_ins, type):
        dict = self.en_instance[user_id]
        dict[type] = ml_ins
        self.en_instance[user_id] = (dict)

    def get_en_instance_all(self, user_id):
        """
        useridを使って全てのアンサンブル用インスタンスを取得する
        """
        return self.en_instance[user_id]

    def get_en_instance_one(self, user_id, type):
        """
        useridとモデル種類名を使って特定のアンサンブル用インスタンスを取得する
        """
        return self.en_instance[user_id][type]

    def init_ml_instance(self, user_id, model_type, objective, path, task) -> None:
        """
        modeltypeにあったmlのインスタンスを取得し、保存する
        """

        if model_type == GBDTClass.get_type():
            ml_ins = GBDTClass(user_id=user_id, objective=objective, original_path=path, task=task)
        elif model_type == NNClass.get_type():
            ml_ins = NNClass(user_id=user_id, objective=objective, original_path=path, task=task)
        elif model_type == RFClass.get_type():
            ml_ins = RFClass(user_id=user_id, objective=objective, original_path=path, task=task)
        else:
            ml_ins = GBDTClass(user_id=user_id, objective=objective, original_path=path, task=task)

        self.set_ml_instance(user_id, ml_ins)

    def nn_ensemble_init(self, user_id, model_type, objective, path, task):
        en_nn = NNClass(user_id=user_id, objective=objective, original_path=path, task=task)
        self.set_ml_instance(user_id, en_nn)

        en_gbdt = GBDTClass(user_id=user_id, objective=objective, original_path=path, task=task)
        en_gbdt.is_ensemble = True
        en_rf = RFClass(user_id=user_id, objective=objective, original_path=path, task=task)
        en_rf.is_ensemble = True

        self.en_instance_init(user_id)
        self.set_en_instance(user_id, en_nn, 'NN')
        self.set_en_instance(user_id, en_gbdt, 'GBDT')
        self.set_en_instance(user_id, en_rf, 'RF')


    def set_predict_instance(self, user_id):
        self.predict_instance[user_id] = PredictionClass()

    def get_predict_instance(self, user_id) -> PredictionClass:
        return self.predict_instance[user_id]