from django.shortcuts import render, redirect
from django.contrib import messages
import csv
import decimal


def index(request):
    return render(request, 'main/index.html')


def info(request):
    return render(request, 'main/info.html')


def redirect_view(request):
    response = redirect('/index')
    return response


def input_form(request):
    return render(request, 'main/input_form.html')


def page2(request):
    s_names = ['S_1', 'S_2', 'S_3', 'S_4', 'S_5']
    w_names = ['W_1', 'W_2', 'W_3', 'W_4', 'W_5']
    o_names = ['O_1', 'O_2', 'O_3', 'O_4', 'O_5']
    t_names = ['T_1', 'T_2', 'T_3', 'T_4', 'T_5']

    s, rs = get_main_data(request, s_names)
    w, rw = get_main_data(request, w_names)
    o, ro = get_main_data(request, o_names)
    t, rt = get_main_data(request, t_names)
    s_len = len(s)
    w_len = len(w)

    try:
        with open('main_data.csv', 'w', newline='') as csvfile:
            fieldnames = ['S', 'RS', 'W', 'RW', 'O', 'RO', 'T', 'RT']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(s_len):
                writer.writerow({'S': s[i], 'RS': rs[i], 'W': w[i], 'RW': rw[i], 'O': o[i], 'RO': ro[i],
                                 'T': t[i], 'RT': rt[i]})
    except IndexError:
        messages.error(request, '* Пожалуйста, заполните одинаковое количество полей в каждой категории, '
                                'в противном случае вычисления будут неверны.')
        return redirect('input_form')

    context = {
        's_weights': s,
        'w_weights': w,
        's_weights_len': s_len,
        'w_weights_len': w_len,
        'sw_weights_len': s_len+w_len,
    }
    return render(request, 'main/page2.html', context)


def page2_output(request):
    s, s_len = load_data('S')
    w, w_len = load_data('W')
    rs, rs_len = load_data('RS')
    rw, rw_len = load_data('RW')
    rsw = []
    rsw.extend(rs)
    rsw.extend(rw)
    weights = []
    weights.extend(s)
    weights.extend(w)
    s_values, s_factor_names = get_factor_values(request, 'Svals', s_len)
    w_values, w_factor_names = get_factor_values(request, 'Wvals', s_len)
    values = []
    values.extend(s_values)
    values.extend(w_values)
    sums = []
    eval = []
    for k in range(len(values)):
        values[k] = list(map(lambda value: '0' if value == '' else value, values[k]))
    for k in range(len(values)):
        s = 0
        for v in values[k]:
            s += float(v)
        sums.append(s)
    for i in range(len(sums)):
        eval.append(decimal.Decimal(sums[i])+decimal.Decimal(rsw[i]))
    for i in range(len(values)):
        values[i].insert(i, None)
    with open('sum_data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(sums)
        writer.writerow(eval)
    context = {
        'weights': weights,
        's_weights_len': s_len,
        'w_weights_len': w_len,
        'sw_weights_len': s_len + w_len,
        'values': values,
        'sums': sums,
    }
    return render(request, 'main/page2_output.html', context)


def page3(request):
    o, o_len = load_data('O')
    t, t_len = load_data('T')
    context = {
        'o_weights': o,
        't_weights': t,
        'o_weights_len': o_len,
        't_weights_len': t_len,
        'ot_weights_len': o_len + t_len,
    }
    return render(request, 'main/page3.html', context)


def page3_output(request):
    o, o_len = load_data('O')
    t, t_len = load_data('T')
    weights = []
    weights.extend(o)
    weights.extend(t)
    o_values, o_factor_names = get_factor_values(request, 'Ovals', o_len)
    t_values, t_factor_names = get_factor_values(request, 'Tvals', o_len)
    values = []
    values.extend(o_values)
    values.extend(t_values)
    for k in range(len(values)):
        values[k] = list(map(lambda value: '0' if value == '' else value, values[k]))
    sums = []
    for k in range(len(values)):
        s = 0
        for v in values[k]:
            s += float(v)
        sums.append(s)
    for i in range(len(values)):
        values[i].insert(i, None)
    with open('sum_data.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(sums)
    context = {
        'weights': weights,
        'o_weights_len': o_len,
        't_weights_len': t_len,
        'ot_weights_len': o_len + t_len,
        'values': values,
        'sums': sums,
    }
    return render(request, 'main/page3_output.html', context)


def page4(request):
    o, o_len = load_data('O')
    t, t_len = load_data('T')
    ro, ro_len = load_data('RO')
    rt, rt_len = load_data('RT')
    sums = load_sums()
    ot_sum = sums[2]
    eval = []
    rot = []
    rot.extend(ro)
    rot.extend(rt)
    for i in range(len(ot_sum)):
        eval.append(decimal.Decimal(ot_sum[i])+decimal.Decimal(rot[i]))
    with open('sum_data.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(eval)
    weights = []
    weights.extend(o)
    weights.extend(t)
    context = {
        'weights': weights,
        'sums': eval,
    }
    return render(request, 'main/page4.html', context)


def page4_output(request):
    o, o_len = load_data('O')
    t, t_len = load_data('T')
    possibilities = request.POST.getlist("pos")
    print(possibilities)
    for k in range(len(possibilities)):
        if possibilities[k] == '':
            possibilities[k] = '0'
    sums = load_sums()
    ot_sum = sums[3]
    pos_eval = []
    for i in range(len(ot_sum)):
        pos_eval.append(decimal.Decimal(ot_sum[i])*decimal.Decimal(possibilities[i]))
    with open('sum_data.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(pos_eval)
    weights = []
    weights.extend(o)
    weights.extend(t)
    context = {
        'weights': weights,
        'sums': ot_sum,
        'possibilities': possibilities,
        'pos_eval': pos_eval,
    }
    return render(request, 'main/page4_output.html', context)


def page5(request):
    s, s_len = load_data('S')
    w, w_len = load_data('W')
    o, o_len = load_data('O')
    t, t_len = load_data('T')
    sums = load_sums()
    sw_sum = sums[1]
    s_eval = []
    half_sw_len = int(len(sw_sum)/2)
    for i in range(half_sw_len):
        s_eval.append(sw_sum[i])
    while len(sw_sum) != half_sw_len:
        sw_sum.remove(sw_sum[0])
    w_eval = sw_sum
    pos_eval = sums[4]
    for k in range(len(pos_eval)):
        pos_eval[k] = abs(decimal.Decimal(pos_eval[k]))
    context = {
        's_weights': s,
        'w_weights': w,
        's_weights_len': s_len,
        'w_weights_len': w_len,
        'sw_weights_len': s_len + w_len,
        'o_weights': o,
        't_weights': t,
        'o_weights_len': o_len,
        't_weights_len': t_len,
        'ot_weights_len': o_len + t_len,
        's_eval': s_eval,
        'w_eval': w_eval,
        'pos_eval': pos_eval
    }
    return render(request, 'main/page5.html', context)


def page5_output(request):
    s, s_len = load_data('S')
    w, w_len = load_data('W')
    o, o_len = load_data('O')
    t, t_len = load_data('T')
    oinf_values, o_factor_names = get_factor_values(request, 'Oinf', o_len)
    tinf_values, t_factor_names = get_factor_values(request, 'Tinf', o_len)
    inf = []
    inf.extend(oinf_values)
    inf.extend(tinf_values)
    for k in range(len(inf)):
        inf[k] = list(map(lambda x: '0' if x == '' else x, inf[k]))
    weights = []
    weights.extend(s)
    weights.extend(w)
    ot_weights = []
    ot_weights.extend(o)
    ot_weights.extend(t)
    sums_inf = []
    sums = load_sums()
    sw_sums = sums[1]
    pos_eval = sums[4]
    for k in range(len(pos_eval)):
        pos_eval[k] = abs(decimal.Decimal(pos_eval[k]))
    final_sums = []
    final_eval = []
    final_o_eval = {}
    final_t_eval = {}
    for i in range(len(sw_sums)):
        mid_sums = []
        s = 0
        for k in range(len(sw_sums)):
            mid_sum = decimal.Decimal(sw_sums[k])*decimal.Decimal(inf[i][k])
            s += mid_sum
            mid_sums.append(mid_sum)
        final_sums.append(s)
        sums_inf.append(mid_sums)
        final_eval.append(s * decimal.Decimal(pos_eval[i]))
        if i < len(sw_sums)/2:
            final_o_eval[ot_weights[i]] = s * decimal.Decimal(pos_eval[i])
        else:
            final_t_eval[ot_weights[i]] = s * decimal.Decimal(pos_eval[i])
    max_o = sorted(final_o_eval.items(), key=lambda x: x[1], reverse=True)[0][0]
    min_o = sorted(final_o_eval.items(), key=lambda x: x[1], reverse=True)[-1][0]
    max_t = sorted(final_t_eval.items(), key=lambda x: x[1], reverse=True)[0][0]
    min_t = sorted(final_t_eval.items(), key=lambda x: x[1], reverse=True)[-1][0]
    context = {
        's_weights': s,
        'w_weights': w,
        'weights': weights,
        's_weights_len': s_len,
        'w_weights_len': w_len,
        'sw_weights_len': s_len + w_len,
        'o_weights': o,
        't_weights': t,
        'o_weights_len': o_len,
        't_weights_len': t_len,
        'ot_weights_len': o_len + t_len,
        'sw_sums': sw_sums,
        'inf': inf,
        'sums_inf': sums_inf,
        'final_eval': final_eval,
        'final_sums': final_sums,
        'pos_eval': pos_eval,
        'max_o': max_o,
        'min_o': min_o,
        'max_t': max_t,
        'min_t': min_t
    }
    return render(request, 'main/page5_output.html', context)


def get_main_data(request, names):
    values = []
    r_values = []
    for name in names:
        value = request.POST.get(name)
        if value is not None and value != '':
            values.append(value)
            r_values.append(request.POST.get('R'+name))
    return values, r_values


def load_data(fieldname):
    values = []
    with open('main_data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            values.append(row[fieldname])
    return values, len(values)


def load_sums():
    sums = []
    with open('sum_data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            sums.append(row)
    return sums


def get_factor_values(request, factor_name, factor_len):
    factor_values = []
    factor_names = []
    for i in range(factor_len):
        unique_factor_name = factor_name+str(i+1)
        factor_values.append(request.POST.getlist(unique_factor_name))
        factor_names.append(unique_factor_name)
    return factor_values, factor_names

