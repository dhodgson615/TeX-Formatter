# TODO

We need to handle cases like this:
```tex
\documentclass{article}
\usepackage[margin=0.25in]{geometry}
\usepackage{amsmath}
\usepackage{xcolor}
\usepackage{forest}
\usepackage{makecell}
\pagenumbering{gobble}

% Red-black node styles
\forestset{
    rbnode/.style={
        circle,
        draw,
        minimum size=1em,
        inner sep=5pt,
        font=\footnotesize\bfseries,
        text=white
    },
    rednode/.style={
        rbnode,
        fill=red!80!black
    },
    blacknode/.style={
        rbnode,
        fill=black
    },
    phantom/.style={
        content={},
        no edge,
        l=0,
        s sep=0pt,
        draw=none,
        fill=none,
        minimum size=0pt,
        inner sep=0pt,
        outer sep=0pt
    }
}

\begin{document}

% Insert 15
\textbf{Insert 15}
\begin{flushleft} \hspace{0.75in}
\begin{forest}
    for tree={l=0.3cm, s sep=0.3cm}
    [15, blacknode]
\end{forest}
\end{flushleft}
\vspace{2em}
\hrule
\vspace{2em}

% Insert 10
\textbf{Insert 10}
\begin{flushleft} \hspace{0.75in}
\begin{forest}
    for tree={l=0.3cm, s sep=0.3cm}
    [15, blacknode
        [10, rednode]
        [, phantom]
    ]
\end{forest}
\end{flushleft}
\vspace{2em}
\hrule
\vspace{2em}

% Insert 20
\textbf{Insert 20}
\begin{flushleft} \hspace{0.75in}
\begin{forest}
    for tree={l=0.3cm, s sep=0.3cm}
    [15, blacknode
        [10, rednode]
        [20, rednode]
    ]
\end{forest}
\end{flushleft}
\vspace{2em}
\hrule
\vspace{2em}

% Insert 30 -> Recolor
\textbf{Insert 30}
\begin{flushleft} \hspace{0.75in}
\begin{tabular}{c@{\hspace{1cm}}c@{\hspace{1cm}}c}
\begin{forest}
    for tree={l=0.3cm, s sep=0.3cm}
    [15, blacknode
        [10, rednode]
        [20, rednode
            [, phantom]
            [30, rednode]
        ]
    ]
\end{forest}
&
$\xrightarrow[\text{Recolor}]{}$
&
\begin{forest}
    for tree={l=0.3cm, s sep=0.3cm}
    [15, blacknode
        [10, blacknode]
        [20, blacknode
            [, phantom]
            [30, rednode]
        ]
    ]
\end{forest}
\end{tabular}
\end{flushleft}
\vspace{2em}
\hrule
\vspace{2em}

\textbf{Insert 25}
\begin{flushleft} \hspace{0.75in}
\begin{tabular}{c@{\hspace{0.5cm}}c@{\hspace{0.5cm}}c@{\hspace{0.5cm}}c@{\hspace{0.5cm}}c}
\begin{forest}
    for tree={l=0.3cm, s sep=0.3cm, baseline}
    [15, blacknode
        [10, blacknode]
        [20, blacknode
            [, phantom]
            [30, rednode
                [25, rednode]
                [, phantom]
            ]
        ]
    ]
\end{forest}
&
$\xrightarrow[\text{Right rotate 30}]{}$
&
\begin{forest}
    for tree={l=0.3cm, s sep=0.3cm, baseline}
    [15, blacknode
        [10, blacknode]
        [20, blacknode
            [, phantom]
            [25, rednode
                [, phantom]
                [30, rednode]
            ]
        ]
    ]
\end{forest}
&
$\xrightarrow[\text{Left rotate 20}]{}$
&
\begin{forest}
    for tree={l=0.3cm, s sep=0.3cm, baseline}
    [15, blacknode
        [10, blacknode]
        [25, blacknode
            [20, rednode]
            [30, rednode]
        ]
    ]
\end{forest}
\end{tabular}
\end{flushleft}
\hrule

\end{document}
```

Currently, the code above renders as this:

```tex
\documentclass{article}
\usepackage[margin=0.25in]{geometry}
\usepackage{amsmath}
\usepackage{xcolor}
\usepackage{forest}
\usepackage{makecell}
\pagenumbering{gobble}

% Red-black node styles
\forestset{
rbnode/.style={
circle,
draw,
minimum size=1em,
inner sep=5pt,
font=\footnotesize\bfseries,
text=white
},
rednode/.style={
rbnode,
fill=red!80!black
},
blacknode/.style={
rbnode,
fill=black
},
phantom/.style={
content={},
no edge,
l=0,
s sep=0pt,
draw=none,
fill=none,
minimum size=0pt,
inner sep=0pt,
outer sep=0pt
}
}

\begin{document}

    % Insert 15
    \textbf{Insert 15}
    \begin{flushleft} \hspace{0.75in}
        \begin{forest}
            for tree={l=0.3cm, s sep=0.3cm}
            [15, blacknode]
        \end{forest}
    \end{flushleft}
    \vspace{2em}
    \hrule
    \vspace{2em}

    % Insert 10
    \textbf{Insert 10}
    \begin{flushleft} \hspace{0.75in}
        \begin{forest}
            for tree={l=0.3cm, s sep=0.3cm}
            [15, blacknode
            [10, rednode]
            [, phantom]
            ]
        \end{forest}
    \end{flushleft}
    \vspace{2em}
    \hrule
    \vspace{2em}

    % Insert 20
    \textbf{Insert 20}
    \begin{flushleft} \hspace{0.75in}
        \begin{forest}
            for tree={l=0.3cm, s sep=0.3cm}
            [15, blacknode
            [10, rednode]
            [20, rednode]
            ]
        \end{forest}
    \end{flushleft}
    \vspace{2em}
    \hrule
    \vspace{2em}

    % Insert 30 -> Recolor
    \textbf{Insert 30}
    \begin{flushleft} \hspace{0.75in}
        \begin{tabular}{c@{\hspace{1cm}}c@{\hspace{1cm}}c}
            \begin{forest}
                for tree={l=0.3cm, s sep=0.3cm}
                [15, blacknode
                [10, rednode]
                [20, rednode
                [, phantom]
                [30, rednode]
                ]
                ]
            \end{forest}
            &
            $\xrightarrow[\text{Recolor}]{}$
            &
            \begin{forest}
                for tree={l=0.3cm, s sep=0.3cm}
                [15, blacknode
                [10, blacknode]
                [20, blacknode
                [, phantom]
                [30, rednode]
                ]
                ]
            \end{forest}
        \end{tabular}
    \end{flushleft}
    \vspace{2em}
    \hrule
    \vspace{2em}

    \textbf{Insert 25}
    \begin{flushleft} \hspace{0.75in}
        \begin{tabular}{c@{\hspace{0.5cm}}c@{\hspace{0.5cm}}c@{\hspace{0.5cm}}c@{\hspace{0.5cm}}c}
            \begin{forest}
                for tree={l=0.3cm, s sep=0.3cm, baseline}
                [15, blacknode
                [10, blacknode]
                [20, blacknode
                [, phantom]
                [30, rednode
                [25, rednode]
                [, phantom]
                ]
                ]
                ]
            \end{forest}
            &
            $\xrightarrow[\text{Right rotate 30}]{}$
            &
            \begin{forest}
                for tree={l=0.3cm, s sep=0.3cm, baseline}
                [15, blacknode
                [10, blacknode]
                [20, blacknode
                [, phantom]
                [25, rednode
                [, phantom]
                [30, rednode]
                ]
                ]
                ]
            \end{forest}
            &
            $\xrightarrow[\text{Left rotate 20}]{}$
            &
            \begin{forest}
                for tree={l=0.3cm, s sep=0.3cm, baseline}
                [15, blacknode
                [10, blacknode]
                [25, blacknode
                [20, rednode]
                [30, rednode]
                ]
                ]
            \end{forest}
        \end{tabular}
    \end{flushleft}
    \hrule

\end{document}
```

This is obviously wrong because the brackets are not properly indented. Right
now, only environments are indented, but we also need to include standard
support for the various bracket types. This is a bit tricky because we need to
be careful about not breaking math mode, but it should be doable by using a
combination of regex and some state tracking to determine whether we're
currently in math mode or not.
