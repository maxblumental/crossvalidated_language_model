from cleaning import clean_text


def test_anchor():
    s = '<a>Hello</a> world'
    assert clean_text(s) == 'Hello world'


def test_anchor_href():
    s = '<a href="http://www.example.com/">Hello</a> world'
    assert clean_text(s) == 'Hello world'


def test_two_anchors():
    s = '<a href="http://www.example.com/">foo</a> bar <a href="https://www.wiki.com/">buzz</a>'
    assert clean_text(s) == 'foo bar buzz'


def test_new_lines():
    s = 'foo\n\nbar'
    assert clean_text(s) == 'foo bar'


def test_code():
    s = 'I think you can use the <code>diff</code> function to your advantage. ' \
        'You could also coerce it to numeric with <code>as.numeric()</code>.'
    clean = clean_text(s)
    assert clean == 'I think you can use the function to your advantage. ' \
                    'You could also coerce it to numeric with.'


def test_latex_expr_with_double_dollar():
    s = 'Doing some testing reveals that residual variance is numerically different from ' \
        '$$ 1 - \text{explained variance}$$ ' \
        'derived from the eigenvalue spectrum.'
    assert clean_text(s) == 'Doing some testing reveals that residual variance is numerically different from ' \
                            'derived from the eigenvalue spectrum.'


def test_latex_expr_with_single_dollar():
    s = 'take $\alpha$ and add it to $\beta$'
    assert clean_text(s) == 'take and add it to'


def test_latex_link():
    s = 'read its [wiki](http://stats.stackexchange.com/tags/self-study/info)'
    assert clean_text(s) == 'read its wiki'


def test_urls():
    s = 'Some papers on it: http://www.jstatsoft.org/v27/i07'
    assert clean_text(s) == 'Some papers on it'

    s = "I do not know how to post the data in stack, here they are: https://we.tl/t-fxXB3eEumG"
    assert clean_text(s) == "I do not know how to post the data in stack, here they are"

    s = "I do not know http://www.journalofdairyscience.org/article/S0022-0302(16)30472-6/references"
    assert clean_text(s) == "I do not know"


def test_back_ticks():
    s = 'Additionally, the `anova(full)` or `anova(full,main)` or `Anova(full,3)` `a\nb` test for all interactions.'
    assert clean_text(s) == 'Additionally, the or or test for all interactions.'


def test_quotes():
    s = 'Did you notice that the title and the question use "equivariant," not "invariant"?'
    assert clean_text(s) == 'Did you notice that the title and the question use equivariant, not invariant?'


def test_nickname():
    s = "@whuber That is again a good point."
    assert clean_text(s) == "That is again a good point."


def test_digits():
    s = "foo 123 bar 312. buzz .05 boo 11.21 wow"
    assert clean_text(s) == "foo bar buzz boo wow"


def test_brackets():
    s = "this (so i think) will work out"
    assert clean_text(s) == "this so i think will work out"


def test_begin_end():
    s = "This is an alternative to the Box-Cox transformations and is defined by \\begin{equation} f(y,\\theta) = \\text{sinh}^{-}(\\theta y)/\\theta = \\log[\\theta y + (\\theta^y^+)^{/}]/\\theta, \\end{equation} where ."
    assert clean_text(s) == "This is an alternative to the Box Cox transformations and is defined by where."

    s = "My work thus far: \\begin{equation} \\begin{array}{lcl} p(x,y) &amp;\\propto &amp; p(x|y) \\\\[ex] &amp;\\propto &amp; \\mathbb{}(-c &lt; |x-y| &lt; c) \\mathbb{}(x,y \\in (,)) \\\\[ex] &amp;\\propto &amp; \\mathbb{}(-c +y &lt; x &lt; c + y) \\mathbb{}(x \\in (,)) \\\\[ex] p(x,y) &amp;\\propto &amp; p(y|x) \\\\[ex] &amp;\\propto &amp; \\mathbb{}(-c &lt; |x-y| &lt; c) \\mathbb{}(x,y \\in (,)) \\\\[ex] &amp;\\propto &amp; \\mathbb{}(-c - x &lt; -y &lt; c - x) \\mathbb{}(x,y \\in (,)) \\\\[ex] &amp;\\propto &amp; \\mathbb{}(c + x &lt; y &lt; -c + x) \\mathbb{}(y \\in (,)) \\\\[ex] \\end{array} \\end{equation} foo bar"
    assert clean_text(s) == "My work thus far: foo bar"


def test_ampersand():
    s = "this &amp; that"
    assert clean_text(s) == "this and that"


def test_pronouns():
    assert clean_text("foo You're bar you're bar") == "foo you are bar you are bar"
    assert clean_text("foo Isn't bar isn't bar") == "foo is not bar is not bar"
    assert clean_text("foo I'm bar i'm bar") == "foo I am bar I am bar"
    assert clean_text("foo I've bar i've bar") == "foo I have bar I have bar"
    assert clean_text("foo It's bar it's bar") == "foo it is bar it is bar"
    assert clean_text("foo Shouldn't bar shouldn't bar") == "foo should not bar should not bar"
    assert clean_text("foo Wouldn't bar wouldn't bar") == "foo would not bar would not bar"
    assert clean_text("foo Aren't bar aren't bar") == "foo are not bar are not bar"
    assert clean_text("foo Don't bar don't bar") == "foo do not bar do not bar"
    assert clean_text("foo Doesn't bar doesn't bar") == "foo does not bar does not bar"
    assert clean_text("foo Didn't bar didn't bar") == "foo did not bar did not bar"
    assert clean_text("foo Haven't bar haven't bar") == "foo have not bar have not bar"
    assert clean_text("foo Weren't bar weren't bar") == "foo were not bar were not bar"
    assert clean_text("foo Wasn't bar wasn't bar") == "foo was not bar was not bar"
    assert clean_text("foo There's bar there's bar") == "foo there is bar there is bar"
    assert clean_text("foo That's bar that's bar") == "foo that is bar that is bar"
    assert clean_text("foo can't bar Can't bar") == "foo can not bar can not bar"


def test_terser_form():
    assert clean_text("foo e.g bar e.g. buzz") == "foo eg bar eg buzz"
    assert clean_text("foo i.e bar i.e. buzz") == "foo ie bar ie buzz"
    assert clean_text("foo TL;DR bar tl;dr buzz") == "foo tldr bar tldr buzz"


def test_asterisk_s():
    assert clean_text("DVM's Dason's DataCamp's") == "DVM Dason DataCamp"


def test_html_tag_code_newline():
    x = '''
    <pre><code>tsExample &lt;- c(1,2,1,2)
    acf(tsExample, plot = FALSE)
    cor(tsExample[1:4], tsExample[1:4])
    cor(tsExample[2:4], tsExample[1:3])
    cor(tsExample[3:4], tsExample[1:2])
    cor(tsExample[4:4], tsExample[1:1])
    
    cor(tsExample[1:4], tsExample[1:4])*(3/4)
    cor(tsExample[2:4], tsExample[1:3])*(2/3)
    cor(tsExample[3:4], tsExample[1:2])*(1/2)
    
    cor(tsExample[1:4], tsExample[1:4])*(4/4)
    cor(tsExample[2:4], tsExample[1:3])*(3/4)
    cor(tsExample[3:4], tsExample[1:2])*(2/4)
    </code></pre>
    '''
    assert clean_text(x) == ''


def test_strip_symbols():
    assert clean_text(" - foo bar  buzz . ") == "foo bar buzz."


def test_hyphen():
    assert clean_text('- foo -bar buzz-buzz-') == "foo bar buzz buzz"
    assert clean_text('- foo bar- buzz-buzz -') == "foo bar buzz buzz"
