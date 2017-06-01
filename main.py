from consensus_algorithm.consensus import compute_consensus_opt1, compute_consensus_opt2
from consensus_algorithm.crossvalidation import check_method
from consensus_algorithm.data import get_views, get_cases
from consensus_algorithm.methods.method1 import method_1
from consensus_algorithm.methods.method2 import method_2

NUMBER_OF_COMPLICATIONS = 13
NUMBER_OF_FOLDS = 10

views = get_views(get_cases(),
                  filter_additional_diseases=[0, 3, 4, 7, 9, 11],
                  filter_operation_type=[1, 2, 3, 4, 5],
                  filter_complications=[x + 1 for x in range(NUMBER_OF_COMPLICATIONS)]
                  )

number_of_symptoms = len(views[0]) - NUMBER_OF_COMPLICATIONS

check_method(method_1, views, compute_consensus_opt1, NUMBER_OF_FOLDS, NUMBER_OF_COMPLICATIONS)
check_method(method_1, views, compute_consensus_opt2, NUMBER_OF_FOLDS, NUMBER_OF_COMPLICATIONS)
check_method(method_2, views, None, NUMBER_OF_FOLDS, NUMBER_OF_COMPLICATIONS)
