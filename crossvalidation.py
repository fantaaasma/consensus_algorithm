def get_folds(views, fold_nuber):
    folds = [[]] * fold_nuber
    for i in range(len(views)):
        folds[i % fold_nuber].append(views[i])
    return folds


def get_stats(real, predicted, number_of_complications):
    stats_for_comp = []
    for c_index in range(number_of_complications):
        tp = 0
        tn = 0
        fp = 0
        fn = 0
        for i in range(len(real)):
            if real[i][c_index] == 1:
                if predicted[i][c_index] == 1:
                    tp += 1
                else:
                    fn += 1
            else:
                if predicted[i][c_index] == 1:
                    fp += 1
                else:
                    tn += 1

        stats_for_comp.append((tp, tn, fp, fn))

    return stats_for_comp


def show_stats(stats, number_of_complications):
    for i in range(number_of_complications):
        print('\nkomplikacja {}'.format(i))
        tp, tn, fp, fn = stats[i]
        accuracy = (tp + tn) / (tp + tn + fp + fn)
        print('poprawność klasyfikacji:', accuracy)
        tn_rate = specificity = tn / (tn + fp)
        print('wskaźnik specyficzności:', specificity)
        if tp + fn:
            tp_rate = sensitivity = tp / (tp + fn)
            print('wskaźnik czułości:', sensitivity)
            gmean = (tp_rate * tn_rate) ** 0.5
            print('wskaźnik średniej geometrycznej czułości i specyficzności:', gmean)
        if fp + tp:
            fp_rate = fp / (fp + tp)
            auc = (1 + tp_rate - fp_rate) / 2
            print('AUC:', auc)


def get_learn_and_test_data(folds, fold_number):
    test_data = None
    learn_data = []
    for i in range(len(folds)):
        if i == fold_number:
            test_data = folds[i]
        else:
            learn_data += folds[i]

    return learn_data, test_data


def check_method(method_fun, views, consensus_fun, number_of_folds, number_of_complications):

    print('{}\nnazwa metody: {}'.format('-' * 20, method_fun.name))

    if consensus_fun:
        print('konsensus spelniajacy kryterium: {}\n'.format(consensus_fun.name))

    folds = get_folds(views, number_of_folds)
    all_real = []
    all_predicted = []
    for i in range(len(folds)):
        print('walidacja krzyżowa fold: {}/{}'.format(i, number_of_folds))
        learn_data, test_data = get_learn_and_test_data(folds, i)
        real, predicted = method_fun(learn_data, test_data, number_of_complications, consensus_fun)
        all_real += real
        all_predicted += predicted

    stats = get_stats(all_real, all_predicted, number_of_complications)
    show_stats(stats, number_of_complications)
