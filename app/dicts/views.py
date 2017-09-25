from flask import render_template, redirect, request
from . import dicts
from .forms import DictsForm


@dicts.route('/', methods=['GET', 'POST'])
def index():
    form = DictsForm()
    if form.validate_on_submit():
        if form.dictname.data == '2':
            return redirect(u'http://dict.youdao.com/w/eng/%s/#keyfrom=dict2.index' % form.englishword.data)
        elif form.dictname.data == '4':
            return redirect(u'http://www.oxfordlearnersdictionaries.com/definition/english/%s_1?q=%s' % (form.englishword.data, form.englishword.data))
        else:
            return redirect('%s%s' % (form.dictname.data, form.englishword.data))
    return render_template('dicts/index.html', form=form)
