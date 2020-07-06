import re

SIMPLE_HTML_TAGS = [
    r'<a href=[^>]+>', r"</a>", r"</b>", r"</blockquote>", r"</br>", r"</del>",
    r"</em>", r"</i>", r"</kbd>", r"</li>", r"</ol>", r"<span[^>]*?>", r'<a>',
    r"</p>", r"</pre>", r"</s>", r'<img src=[^>]+>',
    r"</span>", r"</strike>", r"</strong>", r"</sub>", r"</sup>", r"</ul>",
    r"<b>", r"<blockquote>", r"<br>", r"<del>", r"<em>", r"<hr>", r"<i>",
    r"<kbd>", r"<li>", r"<ol>", r"<p>", r"<pre>", r"<s>",
    r"<strike>", r"<strong>", r"<sub>", r"<sup>", r"<ul>", r"<br\s*/>"
]

AMP_SYMBOL = {'&alpha;', '&ast;', '&asymp;', '&beta;', '&chi;', '&copy;', '&dagger;', '&ddagger;', '&deg;',
              '&emsp;', '&epsilon;', '&frasl;', '&gamma;', '&gt;', '&harr;', '&hellip;', '&infin;', '&keepvar;',
              '&lambda;', '&ldquo;', '&lsquo;', '&lt;', '&macr;', '&mdash;', '&middot;', '&minus;', '&mu;', '&nbsp;',
              '&ndash;', '&ne;', '&oline;', '&plus;', '&quot;', '&rarr;', '&rarrb;', '&rdquo;', '&sect;', '&sigma;',
              '&space;', '&sum;', '&theta;', '&thinsp;', '&times;'}

CODE_BLOCK = re.compile(r'<code>.*?</code>')
LATEX_EXPR = re.compile(r'(\${1,2})[^\$]+\1')
LATEX_LINK = re.compile(r'\[(.*?)\]\(https?://[~0-9a-zA-Z%/&\+\.\?=#_–-]+\)')
PROTOCOL_URL_EXPR = re.compile(r'https?://[~0-9a-zA-Z%/&\+\.\?\(\)=#_–-]+')
BEGIN_END_EXPR = re.compile(r'\\+begin\{(.*?)\}.*?\\+end\{\1\}')


def clean_text(raw_text):
    r = raw_text
    r = re.sub(r'[\n\r]+', ' ', r)
    r = re.sub(r'(?<![a-zA-Z])[Ii]\.[Ee]\.?(?!a-zA-Z)', 'ie', r)
    r = re.sub(r'(?<![a-zA-Z])[Ee]\.[gG]\.?(?!a-zA-Z)', 'eg', r)
    r = re.sub(r'(?i)(?<![a-zA-Z])tl\;dr(?![a-zA-Z])', 'tldr', r)
    r = re.sub(r'(?<![a-zA-Z])[cC]an\'t(?!a-zA-Z)', 'can not', r)
    r = re.sub(r'(?<![a-zA-Z])[wW]ouldn\'t(?!a-zA-Z)', 'would not', r)
    r = re.sub(r'(?<![a-zA-Z])[sS]houldn\'t(?!a-zA-Z)', 'should not', r)
    r = re.sub(r'(?<![a-zA-Z])[yY]ou\'re(?!a-zA-Z)', 'you are', r)
    r = re.sub(r'(?<![a-zA-Z])[Tt]here\'s(?!a-zA-Z)', 'there is', r)
    r = re.sub(r'(?<![a-zA-Z])[Ii]t\'s(?!a-zA-Z)', 'it is', r)
    r = re.sub(r'(?<![a-zA-Z])[Tt]hat\'s(?!a-zA-Z)', 'that is', r)
    r = re.sub(r'(?<![a-zA-Z])[Ii]\'m(?!a-zA-Z)', 'I am', r)
    r = re.sub(r'(?<![a-zA-Z])[Ii]\'ve(?!a-zA-Z)', 'I have', r)
    r = re.sub(r'(?<![a-zA-Z])[Ii]sn\'t(?!a-zA-Z)', 'is not', r)
    r = re.sub(r'(?<![a-zA-Z])[Aa]ren\'t(?!a-zA-Z)', 'are not', r)
    r = re.sub(r'(?<![a-zA-Z])[Dd]on\'t(?!a-zA-Z)', 'do not', r)
    r = re.sub(r'(?<![a-zA-Z])[Dd]oesn\'t(?!a-zA-Z)', 'does not', r)
    r = re.sub(r'(?<![a-zA-Z])[Dd]idn\'t(?!a-zA-Z)', 'did not', r)
    r = re.sub(r'(?<![a-zA-Z])[Hh]aven\'t(?!a-zA-Z)', 'have not', r)
    r = re.sub(r'(?<![a-zA-Z])[wW]eren\'t(?!a-zA-Z)', 'were not', r)
    r = re.sub(r'(?<![a-zA-Z])[wW]asn\'t(?!a-zA-Z)', 'was not', r)
    r = re.sub(r'(?<![a-zA-Z])(\w+)\'s(?!a-zA-Z)', r'\1', r)

    for tag in SIMPLE_HTML_TAGS:
        r = re.sub(tag, '', r)

    r = r.replace('&amp;', 'and')
    for symbol in AMP_SYMBOL:
        r = re.sub(symbol, '', r)

    r = CODE_BLOCK.sub('', r)
    r = BEGIN_END_EXPR.sub('', r)
    r = LATEX_EXPR.sub('', r)
    r = re.sub(LATEX_LINK, r'\1', r)
    r = PROTOCOL_URL_EXPR.sub('', r)
    r = re.sub(r'`[^\`]*?`', '', r)
    r = r.replace('"', '')
    r = re.sub(r'@\w+', '', r)
    r = re.sub(r'[\(\)]', ' ', r)
    r = re.sub(r'(\d+\.\d+|\.\d+|\d+\.|\d+)', '', r)
    r = re.sub(r'\s+', ' ', r)

    r = re.sub(r'[^a-zA-Z]*\?[^a-zA-Z]*', '? ', r)
    r = re.sub(r'[^a-zA-Z]*\.[^a-zA-Z]*', '. ', r)
    r = re.sub(r'[^a-zA-Z]*\![^a-zA-Z]*', '. ', r)
    r = re.sub(r'[^a-zA-Z]*\;[^a-zA-Z]*', '; ', r)
    r = re.sub(r'[^a-zA-Z]*\:[^a-zA-Z]*', ': ', r)
    r = re.sub(r'[^a-zA-Z]*\,[^a-zA-Z]*', ', ', r)

    r = re.sub(r'[^a-zA-Z\.\?\;\:\,]+', ' ', r)

    r = r.lstrip('.,:;? ')
    r = r.rstrip(',:; ')

    return r
