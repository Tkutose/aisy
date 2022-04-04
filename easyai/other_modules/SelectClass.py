from msilib.schema import Extension

from django.db import connection
from easyai.models import Activation, CategoricalMethods, CategoricalTransformation, DoneCategorical, DoneDeleteString, DoneMissing, DoneReplaceString, EnsembleCompositions, EnsembleEvaluations, EnsembleMethods, Extensions, FeatureValues, LearnPlan, Loss, MachineLearning, ModelInfo, ModelTypes, Models, ModelsByUser, Optimizer, Tasks, OriginalData, MissingMethods, Users

class SelectClass():
    def select_original_use_index(self, id):
        return OriginalData.objects.get(pk=id)

    def select_extension_use_name(self, extensions_name):
        return Extensions.objects.get(extensions_name=extensions_name)

    def select_extension_use_index(self, extensions_id):
        return Extensions.objects.get(id=extensions_id)

    def select_feature_value_use_index(self, id):
        return FeatureValues.objects.get(id=id)

    def select_model_types_use_type_name(self, type):
        return ModelTypes.objects.get(type=type)

    def select_task_use_name(self, task_name):
        return Tasks.objects.get(task_name=task_name)

    def select_missing_method_use_name(self, method_name):
        return MissingMethods.objects.get(method_name=method_name)

    def select_categorical_method_use_name(self, method_name):
        return CategoricalMethods.objects.get(method_name=method_name)

    def select_categorical_transformation_use_feature_id(self, feature_id):
        feature_value_obj = FeatureValues.objects.get(id=feature_id)
        return [value for value in CategoricalTransformation.objects.filter(feature_value=feature_value_obj)]

    def select_loss_use_name(self, function_name):
        return Loss.objects.get(function_name=function_name)

    def select_machine_learning_use_index(self, id):
        return MachineLearning.objects.get(id=id)

    def select_models_use_index(self, id) -> Models:
        return Models.objects.get(id=id)

    def select_activation_use_name(self, activation_name):
        return Activation.objects.get(activation_name=activation_name)

    def select_optimizer_use_name(self, optimizer_name):
        return Optimizer.objects.get(optimizer_name=optimizer_name)

    def select_ensemble_method_use_name(self, method_name):
        return EnsembleMethods.objects.get(method_name=method_name)

    def select_ensemble_evaluations_use_index(self, id):
        return EnsembleEvaluations.objects.get(id=id)

    def select_ensemble_conposition_use_en_id(self, id):
        en_obj = EnsembleEvaluations.objects.get(id=id)
        return [value for value in EnsembleCompositions.objects.filter(ensemble_evaluation=en_obj)]

    def select_models_by_user_use_user_id(self, id) -> ModelsByUser:
        return [value for value in ModelsByUser.objects.filter(user_id=id)]

    def select_learn_plan_use_index(self, id) ->LearnPlan :
        return LearnPlan.objects.get(id=id)

    def select_done_delete_string_use_index(self, id) -> DoneDeleteString:
        return [value for value in DoneDeleteString.objects.filter(model_id=id)]

    def select_done_replace_string_use_index(self, id) -> DoneReplaceString:
        return [value for value in DoneReplaceString.objects.filter(model_id=id)]

    def select_done_categorical_use_index(self, id) -> DoneCategorical:
        return [value for value in DoneCategorical.objects.filter(model_id=id)]

    def select_done_missing_use_index(self, id) -> DoneMissing:
        return [value for value in DoneMissing.objects.filter(model_id=id)]

    def select_model_info_use_index(self, id) -> ModelInfo:
        return  ModelInfo.objects.get(model_id=id)

    def select_model_info_use_en_id(self, id) -> ModelInfo:
        return [value for value in ModelInfo.objects.filter(ensemble_id=id)]