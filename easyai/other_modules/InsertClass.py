from easyai.models import CategoricalTransformation, DivisionData, EnsembleCompositions, EnsembleEvaluations, FeatureValues, GradientBoostingDecisionTree, MachineLearning, ModelEvaluations, Models, NeuralNetwork, RandomForest, ReplaceString, Standardization, Users, Extensions, OriginalData, DeleteString, Tasks, MissingProcessing
from easyai.other_modules import SingletonClass

class InsertClass(SingletonClass):
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__init__()
        return cls._instance
    
    def __init__(self) -> None:
        self.original_ids = {}

    def set_original_id(self, user_id, id):
        self.original_ids[user_id] = id

    def get_original_id(self, user_id):
        return self.original_ids[user_id]

    def insert_OriginalData(self, path, file_name, extension_name, user_id):
        """
        唯一mlのインスタンスから呼び出し不可。
        """
        user_obj = Users.objects.get(pk=user_id)
        extension_obj = Extensions.objects.get(extensions_name=extension_name)
        original_data_obj = OriginalData(
            path=path, file_name=file_name, extension=extension_obj, user=user_obj)
        original_data_obj.save()
        self.set_original_id(user_id, original_data_obj.id)


    def insert_FeatureValues(self, original_obj, objective, model_type_obj, task_obj) ->int:
        """
        挿入したレコードの主キーを返す
        """
        feature_values_obj = FeatureValues(objective=objective, original_data=original_obj, model_type=model_type_obj, task=task_obj)
        feature_values_obj.save()
        return feature_values_obj.id

    def insert_DeleteString(self, feature_obj, delete_list):
        for delete_column in delete_list:
            delete_string_obj = DeleteString(delete_column=delete_column, feature_value=feature_obj)
            delete_string_obj.save()

    def insert_ReplaceString(self, column_name, before, after, feature_obj, regex=True):
        regex_value = 1 if regex == True else 0
        replace_string_obj = ReplaceString(column_name=column_name, replace_before=before, replace_after=after, is_regex=regex_value, feature_value=feature_obj)
        replace_string_obj.save()

    def insert_MissingProcessing(self, missing_method_obj, column_name, value, feature_obj):
        missing_processing_obj = MissingProcessing(
                column_name=column_name, missing_method=missing_method_obj, replace_str=value, feature_value=feature_obj
                )
        missing_processing_obj.save()

    def insert_CategoricalTransformation(self, column, before, after, feature_obj, categorical_method_obj):
        categorical_obj = CategoricalTransformation(
            column_name=column,
            before_value=before,
            after_value=after,
            feature_value=feature_obj,
            categorical_method=categorical_method_obj,
        )
        categorical_obj.save()

    def insert_Standardization(self, is_standardization, feature_obj):
        standardization_obj = Standardization(
            is_standardization=is_standardization,
            feature_value=feature_obj
        )
        standardization_obj.save()
        
    def insert_DivisionData(self, random_state, test_size, feature_value_obj):
        division_data_obj = DivisionData(
            random_state=random_state,
            test_size=test_size,
            feature_value=feature_value_obj
        )
        division_data_obj.save()

    def insert_MachineLearning(self, loss_value, val_loss_value, loss_obj, feature_value_obj) -> int:
        """
        挿入したレコードの主キーを返す
        """
        machine_learning_obj = MachineLearning(
            loss_value=loss_value,
            val_loss_value=val_loss_value,
            loss=loss_obj,
            feature_value=feature_value_obj,
            )
        machine_learning_obj.save()
        return machine_learning_obj.id

    def insert_Models(self, path, extension_obj, machine_learning_obj)-> int:
        """
        挿入したレコードの主キーを返す
        """
        models_obj = Models(
            path=path,
            extension=extension_obj,
            machine_learning=machine_learning_obj
            )
        models_obj.save()
        return models_obj.id

    def insert_GradientBoostingDecisionTree(self, model_obj, learn_rate, max_depth, num_round, early_round):
        gbdt_obj = GradientBoostingDecisionTree(
            model=model_obj,
            learn_rate=learn_rate,
            max_depth=max_depth,
            num_round=num_round,
            early_stopping_round=early_round,
        )
        gbdt_obj.save()

    def insert_NeuralNetwork(self, model_obj, num_layers, units, hidden_activation_obj, optimizer_obj, 
            is_batchnormalization, is_early_stopping, min_delta, patience, is_dropout, 
            epoch, batch_size, learn_rate, output_activation_obj):

        nn_obj = NeuralNetwork(
            model=model_obj,
            num_layers=num_layers,
            units=units,
            hidden_activation=hidden_activation_obj,
            optimizer=optimizer_obj,
            is_batchnormalization=is_batchnormalization,
            is_early_stopping=is_early_stopping,
            min_delta=min_delta,
            patience=patience,
            is_dropout=is_dropout,
            epoch=epoch,
            batch_size=batch_size,
            learn_rate=learn_rate,
            output_activation=output_activation_obj
        )
        nn_obj.save()


    def insert_no_early_NeuralNetwork(self, model_obj, num_layers, units, hidden_activation_obj, optimizer_obj, 
            is_batchnormalization, is_early_stopping, is_dropout, 
            epoch, batch_size, learn_rate, output_activation_obj):

        nn_obj = NeuralNetwork(
            model=model_obj,
            num_layers=num_layers,
            units=units,
            hidden_activation=hidden_activation_obj,
            optimizer=optimizer_obj,
            is_batchnormalization=is_batchnormalization,
            is_early_stopping=is_early_stopping,
            min_delta=-1,
            patience=-1,
            is_dropout=is_dropout,
            epoch=epoch,
            batch_size=batch_size,
            learn_rate=learn_rate,
            output_activation=output_activation_obj
        )
        nn_obj.save()

    def insert_RandomForest(self, model_obj, random_state, max_depth, max_features, min_samples_split, n_estimators):
        rf_obj = RandomForest(
            model = model_obj,
            random_state = random_state,
            max_depth = max_depth,
            max_features = max_features,
            min_samples_split = min_samples_split,
            n_estimators = n_estimators
        )
        rf_obj.save()

    def insert_ModelEvaluations(self, model_obj, mae=-1, mse=-1, rmse=-1, 
            coefficient_of_determination=-1, accuracy_score=-1, precision_score=-1, 
            recall_score=-1, f1_score=-1, logloss=-1, auc=-1, multi_class_accuracy=-1, 
            mean_f1=-1, macro_f1=-1, micro_f1=-1, multi_class_logloss=-1):

        model_eval_obj = ModelEvaluations(
            model=model_obj,
            mae=mae,
            mse=mse,
            rmse=rmse,
            coefficient_of_determination=coefficient_of_determination,
            accuracy_score=accuracy_score,
            precision_score=precision_score,
            recall_score=recall_score,
            f1_score=f1_score,
            logloss=logloss,
            auc=auc,
            multi_class_accuracy=multi_class_accuracy,
            mean_f1=mean_f1,
            macro_f1=macro_f1,
            micro_f1=micro_f1,
            multi_class_logloss=multi_class_logloss
        )
        model_eval_obj.save()

    def insert_EnsembleEvaluations(self, ensemble_method_obj, mae=-1, mse=-1, rmse=-1,
                                coefficient_of_determination=-1, accuracy_score=-1, precision_score=-1,
                                recall_score=-1, f1_score=-1, logloss=-1, auc=-1, multi_class_accuracy=-1,
                                mean_f1=-1, macro_f1=-1, micro_f1=-1, multi_class_logloss=-1):
        """
        挿入したレコードの主キーを返す
        """
        eval_obj = EnsembleEvaluations(
            ensemble_method = ensemble_method_obj,
            mae=mae,
            mse=mse,
            rmse=rmse,
            coefficient_of_determination=coefficient_of_determination,
            accuracy_score=accuracy_score,
            precision_score=precision_score,
            recall_score=recall_score,
            f1_score=f1_score,
            logloss=logloss,
            auc=auc,
            multi_class_accuracy=multi_class_accuracy,
            mean_f1=mean_f1,
            macro_f1=macro_f1,
            micro_f1=micro_f1,
            multi_class_logloss=multi_class_logloss
        )
        eval_obj.save()
        return eval_obj.id


    def insert_EnsembleCompositions(self, model_obj, ensemble_obj):
        conposition_obj = EnsembleCompositions(
            model = model_obj,
            ensemble_evaluation = ensemble_obj
        )
        conposition_obj.save()