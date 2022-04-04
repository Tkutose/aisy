# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Activation(models.Model):
    activation_name = models.CharField(max_length=20)

    class Meta:
        db_table = 'activation'


class CategoricalMethods(models.Model):
    method_name = models.CharField(unique=True, max_length=50)

    class Meta:
        db_table = 'categorical_methods'


class CategoricalTransformation(models.Model):
    column_name = models.CharField(max_length=50)
    before_value = models.CharField(max_length=100)
    after_value = models.DecimalField(max_digits=20, decimal_places=14)
    feature_value = models.ForeignKey('FeatureValues', models.DO_NOTHING)
    categorical_method = models.ForeignKey(
        CategoricalMethods, models.DO_NOTHING)

    class Meta:
        db_table = 'categorical_transformation'


class DeleteOutliers(models.Model):
    column_name = models.CharField(max_length=50)
    delete_value = models.DecimalField(max_digits=20, decimal_places=10)
    feature_value = models.ForeignKey('FeatureValues', models.DO_NOTHING)

    class Meta:
        db_table = 'delete_outliers'


class DeleteString(models.Model):
    delete_column = models.CharField(max_length=50)
    feature_value = models.ForeignKey('FeatureValues', models.DO_NOTHING)

    class Meta:
        db_table = 'delete_string'


class DivisionData(models.Model):
    random_state = models.DecimalField(max_digits=5, decimal_places=0)
    test_size = models.DecimalField(max_digits=4, decimal_places=3)
    feature_value = models.ForeignKey('FeatureValues', models.DO_NOTHING)

    class Meta:
        db_table = 'division_data'


class EnsembleCompositions(models.Model):
    model = models.ForeignKey('Models', models.DO_NOTHING)
    ensemble_evaluation = models.ForeignKey('EnsembleEvaluations', models.DO_NOTHING)

    class Meta:
        db_table = 'ensemble_compositions'
        unique_together = (('ensemble_evaluation', 'model'),)


class EnsembleEvaluations(models.Model):
    ensemble_method = models.ForeignKey('EnsembleMethods', models.DO_NOTHING)
    # Field name made lowercase.
    mae = models.DecimalField(
        db_column='MAE', max_digits=20, decimal_places=10)
    # Field name made lowercase.
    mse = models.DecimalField(
        db_column='MSE', max_digits=20, decimal_places=10)
    # Field name made lowercase.
    rmse = models.DecimalField(
        db_column='RMSE', max_digits=20, decimal_places=10)
    coefficient_of_determination = models.DecimalField(
        max_digits=10, decimal_places=9)
    accuracy_score = models.DecimalField(max_digits=10, decimal_places=9)
    precision_score = models.DecimalField(max_digits=10, decimal_places=9)
    recall_score = models.DecimalField(max_digits=10, decimal_places=9)
    f1_score = models.DecimalField(max_digits=10, decimal_places=7)
    logloss = models.DecimalField(max_digits=10, decimal_places=9)
    # Field name made lowercase.
    auc = models.DecimalField(db_column='AUC', max_digits=10, decimal_places=9)
    multi_class_accuracy = models.DecimalField(max_digits=10, decimal_places=9)
    mean_f1 = models.DecimalField(max_digits=10, decimal_places=7)
    macro_f1 = models.DecimalField(max_digits=10, decimal_places=7)
    micro_f1 = models.DecimalField(max_digits=10, decimal_places=7)
    multi_class_logloss = models.DecimalField(max_digits=12, decimal_places=9)

    class Meta:
        db_table = 'ensemble_evaluations'


class EnsembleMethods(models.Model):
    method_name = models.CharField(unique=True, max_length=20)

    class Meta:
        db_table = 'ensemble_methods'


class Extensions(models.Model):
    extensions_name = models.CharField(unique=True, max_length=4)

    class Meta:
        db_table = 'extensions'


class FeatureValues(models.Model):
    objective = models.CharField(max_length=50)
    original_data = models.ForeignKey('OriginalData', models.DO_NOTHING)
    model_type = models.ForeignKey('ModelTypes', models.DO_NOTHING)
    task = models.ForeignKey('Tasks', models.DO_NOTHING)

    class Meta:
        db_table = 'feature_values'


class GradientBoostingDecisionTree(models.Model):
    model = models.OneToOneField('Models', models.DO_NOTHING, primary_key=True)
    learn_rate = models.DecimalField(max_digits=21, decimal_places=20)
    max_depth = models.DecimalField(max_digits=2, decimal_places=0)
    num_round = models.DecimalField(max_digits=4, decimal_places=0)
    early_stopping_round = models.DecimalField(max_digits=4, decimal_places=0)

    class Meta:
        db_table = 'gradient_boosting_decision_tree'


class Loss(models.Model):
    function_name = models.CharField(unique=True, max_length=50)

    class Meta:
        db_table = 'loss'


class MachineLearning(models.Model):
    loss_value = models.DecimalField(max_digits=20, decimal_places=10)
    val_loss_value = models.DecimalField(max_digits=20, decimal_places=10)
    loss = models.ForeignKey(Loss, models.DO_NOTHING)
    feature_value = models.ForeignKey(FeatureValues, models.DO_NOTHING)

    class Meta:
        db_table = 'machine_learning'


class MissingMethods(models.Model):
    method_name = models.CharField(unique=True, max_length=50)

    class Meta:
        db_table = 'missing_methods'


class MissingProcessing(models.Model):
    column_name = models.CharField(max_length=50)
    missing_method = models.ForeignKey(MissingMethods, models.DO_NOTHING)
    replace_str = models.CharField(max_length=100, blank=True, null=True)
    feature_value = models.ForeignKey(FeatureValues, models.DO_NOTHING)

    class Meta:
        db_table = 'missing_processing'


class ModelEvaluations(models.Model):
    model = models.ForeignKey('Models', models.DO_NOTHING)
    # Field name made lowercase.
    mae = models.DecimalField(
        db_column='MAE', max_digits=20, decimal_places=10)
    # Field name made lowercase.
    mse = models.DecimalField(
        db_column='MSE', max_digits=20, decimal_places=10)
    # Field name made lowercase.
    rmse = models.DecimalField(
        db_column='RMSE', max_digits=20, decimal_places=10)
    coefficient_of_determination = models.DecimalField(
        max_digits=10, decimal_places=9)
    accuracy_score = models.DecimalField(max_digits=10, decimal_places=9)
    precision_score = models.DecimalField(max_digits=10, decimal_places=9)
    recall_score = models.DecimalField(max_digits=10, decimal_places=9)
    f1_score = models.DecimalField(max_digits=10, decimal_places=7)
    logloss = models.DecimalField(max_digits=10, decimal_places=9)
    # Field name made lowercase.
    auc = models.DecimalField(db_column='AUC', max_digits=10, decimal_places=9)
    multi_class_accuracy = models.DecimalField(max_digits=10, decimal_places=9)
    mean_f1 = models.DecimalField(max_digits=10, decimal_places=7)
    macro_f1 = models.DecimalField(max_digits=10, decimal_places=7)
    micro_f1 = models.DecimalField(max_digits=10, decimal_places=7)
    multi_class_logloss = models.DecimalField(max_digits=12, decimal_places=9)

    class Meta:
        db_table = 'model_evaluations'


class ModelTypes(models.Model):
    type = models.CharField(unique=True, max_length=50)

    class Meta:
        db_table = 'model_types'


class Models(models.Model):
    path = models.CharField(unique=True, max_length=50)
    extension = models.ForeignKey(Extensions, models.DO_NOTHING)
    machine_learning = models.ForeignKey(MachineLearning, models.DO_NOTHING)

    class Meta:
        db_table = 'models'


class NeuralNetwork(models.Model):
    model = models.OneToOneField    (Models, models.DO_NOTHING, primary_key=True)
    num_layers = models.DecimalField(max_digits=2, decimal_places=0)
    units = models.DecimalField(max_digits=4, decimal_places=0)
    hidden_activation = models.ForeignKey(
        Activation, models.DO_NOTHING, related_name='hidden_activation')
    optimizer = models.ForeignKey('Optimizer', models.DO_NOTHING)
    is_batchnormalization = models.IntegerField()
    is_early_stopping = models.IntegerField()  # This field type is a guess.
    min_delta = models.DecimalField(max_digits=6, decimal_places=5)
    patience = models.DecimalField(max_digits=4, decimal_places=0)
    is_dropout = models.IntegerField()  # This field type is a guess.
    epoch = models.DecimalField(max_digits=4, decimal_places=0)
    batch_size = models.DecimalField(max_digits=4, decimal_places=0)
    learn_rate = models.DecimalField(max_digits=21, decimal_places=20)
    output_activation = models.ForeignKey(
        Activation, models.DO_NOTHING, related_name='output_activation')

    class Meta:
        db_table = 'neural_network'



class Optimizer(models.Model):
    optimizer_name = models.CharField(unique=True, max_length=20)

    class Meta:
        db_table = 'optimizer'


class OriginalData(models.Model):
    path = models.CharField(unique=True, max_length=50)
    file_name = models.CharField(max_length=50)
    extension = models.ForeignKey(Extensions, models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)

    class Meta:
        db_table = 'original_data'

class RandomForest(models.Model):
    model = models.OneToOneField(Models, models.DO_NOTHING, primary_key=True)
    random_state = models.DecimalField(max_digits=5, decimal_places=0)
    max_depth = models.DecimalField(max_digits=2, decimal_places=0)
    max_features = models.DecimalField(max_digits=3, decimal_places=0)
    min_samples_split = models.DecimalField(max_digits=2, decimal_places=0)
    n_estimators = models.DecimalField(max_digits=3, decimal_places=0)

    class Meta:
        db_table = 'random_forest'


class ReplaceString(models.Model):
    column_name = models.CharField(max_length=50)
    replace_before = models.CharField(max_length=50)
    replace_after = models.CharField(max_length=50)
    is_regex = models.IntegerField()  # This field type is a guess.
    feature_value = models.ForeignKey(FeatureValues, models.DO_NOTHING)

    class Meta:
        db_table = 'replace_string'


class Standardization(models.Model):
    is_standardization = models.IntegerField()  # This field type is a guess.
    feature_value = models.ForeignKey(FeatureValues, models.DO_NOTHING)

    class Meta:
        db_table = 'standardization'


class Tasks(models.Model):
    task_name = models.CharField(unique=True, max_length=20)

    class Meta:
        db_table = 'tasks'


class Users(models.Model):
    username = models.CharField(unique=True, max_length=20)
    password = models.CharField(max_length=20)

    class Meta:
        db_table = 'users'


"""
views
"""


class ModelsByUser(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    model_path = models.CharField(
        max_length=50, db_collation='utf8mb4_0900_ai_ci')
    model_type = models.CharField(
        max_length=50, db_collation='utf8mb4_0900_ai_ci', blank=True, null=True)
    file_name = models.CharField(
        max_length=50, db_collation='utf8mb4_0900_ai_ci', blank=True, null=True)
    user_id = models.PositiveIntegerField(blank=True, null=True)
    user_name = models.CharField(
        max_length=20, db_collation='utf8mb4_0900_ai_ci', blank=True, null=True)
    ensemble_id = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'models_by_user'


class LearnPlan(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    objective = models.CharField(
        max_length=50, db_collation='utf8mb4_0900_ai_ci', blank=True, null=True)
    task = models.CharField(
        max_length=20, db_collation='utf8mb4_0900_ai_ci', blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'learn_plan'


class DoneDeleteString(models.Model):
    model_id = models.PositiveIntegerField(primary_key=True)
    delete_column = models.CharField(max_length=50, db_collation='utf8mb4_0900_ai_ci', blank=True, null=True)     

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'done_delete_string'


class DoneReplaceString(models.Model):
    model_id = models.PositiveIntegerField(primary_key=True)
    column_name = models.CharField(max_length=50, db_collation='utf8mb4_0900_ai_ci', blank=True, null=True)       
    before_str = models.CharField(max_length=50, db_collation='utf8mb4_0900_ai_ci', blank=True, null=True)        
    after_str = models.CharField(max_length=50, db_collation='utf8mb4_0900_ai_ci', blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'done_replace_string'


class DoneCategorical(models.Model):
    model_id = models.PositiveIntegerField(primary_key=True)
    column_name = models.CharField(max_length=50, db_collation='utf8mb4_0900_ai_ci', blank=True, null=True)       
    before_str = models.CharField(max_length=100, db_collation='utf8mb4_0900_ai_ci', blank=True, null=True)       
    after_str = models.DecimalField(max_digits=20, decimal_places=14, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'done_categorical'

class DoneMissing(models.Model):
    model_id = models.PositiveIntegerField(primary_key=True)
    column_name = models.CharField(max_length=50, db_collation='utf8mb4_0900_ai_ci', blank=True, null=True)       
    fill_str = models.CharField(max_length=100, db_collation='utf8mb4_0900_ai_ci', blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'done_missing'


class ModelInfo(models.Model):
    model_id = models.PositiveIntegerField(primary_key=True)
    model_type = models.CharField(
        max_length=50, db_collation='utf8mb4_0900_ai_ci', blank=True, null=True)
    ensemble_id = models.PositiveIntegerField(blank=True, null=True)
    original_path = models.CharField(
        max_length=50, db_collation='utf8mb4_0900_ai_ci', blank=True, null=True)
    user_id = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'model_info'
