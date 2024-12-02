---
title: "Nonlinear Calculi"
date: 2024-12-02
---

# Nonlinear Calculi

Inciting thought: (c.f. Carl Bender lectures) Taylor series also determine lots of continued function representations (e.g., continued fraction $f(x) = \frac{b_0}{1 - \frac{b_1 x}{1 - \frac{b_2 x}{\dots}}}$). I also was reading some of Scott Garrabrant's stuff about geometric expectations/calculus, which got me to thinking about what completes the analogy 

"$\text{Taylor series} : \text{linear derivative} :: \text{Continued fraction} : ??$"

TL;DR the answer is approximately what are called Taylor polynomials over "division rings" on $\mathbb{R}$, though as we'll discuss them, we usually won't represent them as polynomials. I'm not sure if this is too commonly known in applied circles, but it's mainstream enough in math. The difference in emphasis I want to present here is using these as a potential technique for solving ODEs, etc.

## Geometric Calculus = Foreshadowing

Geometric calculus is calculus but where 'addition' is replaced with multiplication. This is possibly familiar if you know the *logarithmic derivative* and *product integral* (both of which at least have Wikipedia pages).

Geometric calculus has the nice fact that you can take logs, do normal calculus, then exponentiate. So, for example, the geometric integral operator is:

$$
J_G f = e^{J \left[ \ln f \right]}
$$

and the geometric derivative operator is

$$
D_G f = e^{D \left[ \ln f \right]} = e^{\left( \frac{Df}{f} \right)}
$$

(the traditional logarithmic derivative is the logarithm of that).

Scott Garrabrant has a good series on geometric thinking, geometric expectations, etc. The basic thrust of it is that there are certain times where things are just begging to be multiplied together, and we end up doing log-then-stuff-then-exp, so that we can use normal calculus tools which are additive—but really this geometric structure is _natural_ and we should learn to think with "product integral" as the primitive, not "$e^{\int \ln f}$".

We can do this way more generally too—I had to learn an appreciable bit of purer-than-I'm-used-to math stuff to really elaborate on this idea of 'naturalness', so:

1. Possible pure math warning if you're an applied-math person.
2. I'm quite cavalier in seeing what I can get out of my equations and not disposed right now to try and be rigorous and parsimonious about what conditions/axioms I'm using—please take the use of any pure math term like "division ring" to mean "something like a division ring, maybe plus or minus some axioms." And please watch out for any mistakes induced by this cavalierness—I’m just here to have fun :)

## How to Summon Forth Your Very Own Calculus Monstrosity!
*(Feel free to skip below to the examples if you want to see where this is going before reading the ingredients list!)*

The fundamental approach is that we start with some binary operation that takes the place of addition, and call this $\oplus$. $\oplus$ needs to be such that you can also define the following laundry list:

- $\oplus$ is associative, commutative, has an identity, and permits unique additive inverses (and $\ominus$ defined using the additive inverse). In this post $(-a)$ will always default to meaning the additive inverse of $a$, NOT the actual real negative of $a$ over the reals.
- $\otimes$ (generalized multiplication) must be distributive over $\oplus$ and must have an identity, $e_{\otimes}$. It also has to allow division $\oslash$.
- $\oslash$ (only needs to work on one side: $(a \oslash b) \otimes b = a$), which is defined except for when the right argument is $e_{\otimes}$.

Some additional nice geometric properties follow if we can define a positive cone $P_{\oplus}$ and a metric $d_{\oplus}$. I'm not sure if these are _necessary_ (I haven't checked any examples that don't have this), but they go a long way towards explaining what structure is at work and probably are necessary for this to be _useful_.

**Positive Cone:** Generalizes the ordering relation of $<, >, =$. The positive cone set $P$ satisfies the axioms:

- $P \oplus P$ and $P \otimes P$ are both subsets of $P$,
- $P \cap (\text{negative } P) = e_{\otimes}$,
- $P \cup (\text{negative } P) = \mathbb{R} - \{ e_{\oplus} \}$.

This gives you the total order $<_{\oplus}$ and its congeners.

This lets you define:

$$
\text{abs}(x) = 
\begin{cases} 
x & \text{if } x \in P \\
-x & \text{otherwise}
\end{cases}
$$

In turn, giving you at least one metric $d_{\oplus}$. You can presumably do just fine with other metrics too.

The last thing I'll use is a notion of intervals and the natural (Haar) measure:

$$
d\mu_{\oplus}(x) = \frac{dx}{\| \frac{d}{dg} (x \oplus g) \|_{g=e_{\oplus}}}
$$

This basically lets us express the $\oplus$-integral in terms of the regular additive one; note $\frac{d}{dx}$ there is the normal additive derivative. $\mu_{\oplus}$ is defined by the fact that if you feed it an interval, it'll give you an answer which is invariant under action by $\oplus$-ing anything to both ends of the interval—the same way $(1,10)$ is the same length as $(1 \oplus 10, 10 \oplus 10) = (11,20)$, just with $\oplus$ instead. In the geometric case, _multiplying_ both interval-ends by 10 will give you the length wrt $\mu$ before and after.

This induces a distance:

$$
d_{\oplus}(a, b) = \int_{[a, b]} d\mu_{\oplus}(x)
$$

"The Haar measure of the interval $[a, b]$"

This kind of list might feel similar to how we talk about coordinate transformations in tensor calculus. More on this in a bit ;)

I was tempted to think about this in a "space 1" vs "space 2" way, with the "arithmetic" vs "new" calculus - this is maybe sorta true, but I ended up getting more wrong than right thinking this way. Instead, like in relativity when we have some geometric thing that is honest-to-god invariant, like a temperature field or something, in our game here the numbers are 'invariant': $3 \oplus 2 \neq 3 + 2$ in general, but any function that can be written in terms of traditional operations can be written in the new ones, like

$$
f_+(x) = x^{12} \quad \longrightarrow \quad f_{\oplus}(x) = x \otimes (e^{12})
$$

(this notation disagrees with what we'll use later, fyi)

The RHS is in geometric form, and $e^{12}$ should be considered some number, not any geometric reinterpretation of the exponentiation or anything like that.

These two functions take in an $x$ and output $f(x)$ - they're literally equal, just written differently.

Now for the recipes!!

### Derivative

$$
D_{\oplus} f(x) = \lim_{\bar{x} \to x} [f(\bar{x}) \ominus f(x)] \oslash d_{\oplus}(x, \bar{x})
$$

**Important Property 1  (Distributive over $\oplus$):**

$$
D_{\oplus} [f \oplus g] = D_{\oplus} [f] \oplus D_{\oplus} [g]
$$

**Proof:**

$$
D_{\oplus} [f \oplus g](x) = \lim_{\bar{x} \to x} [(f(\bar{x}) \oplus g(\bar{x})) \ominus (f(x) \oplus g(x))] \oslash d_{\oplus}(x, \bar{x})
$$

Because $(a \oplus b) \oslash c = (a \oslash c) \oplus (b \oslash c)$ and associativity of $\oplus$, you can separate the limits. Note this doesn't require anything in particular of the metric $d$.

**Important Property 2 (Leibniz over $\otimes$):**

$$
D_{\oplus} [f \otimes g] = (D_{\oplus} [f] \otimes g) \oplus (f \otimes D_{\oplus} [g])
$$

**Proof:**

$$
D_{\oplus} [f \otimes g](x) = \lim_{\bar{x} \to x} [(f(\bar{x}) \otimes g(\bar{x})) \ominus (f(x) \otimes g(x))] \oslash d_{\oplus}(x, \bar{x})
$$

Add-and-subtract to get the numerator in terms of $[f(\bar{x}) - f(x)]$ and $[g(\bar{x}) - g(x)]$, separate the limits, and end up with a term like $[f(\bar{x}) - f(x)] \cdot [g(\bar{x}) - g(x)]$, which is $\mathcal{O}(h^2)$ and thus vanishes.

**Some Other Things That Interestingly "Don't Work":**

- Anything using a number $h$ approaching either $0$ or $e_{\otimes}$ for the limit.
- Using $\oplus$ and $\ominus$ to add/subtract $h$ _within_ the function arguments.

*(I haven't investigated this any further, but it seems to me like using another distance $d(x,\bar{x})$ should get you another version of the derivative which should also work just fine as a derivative - I'm just taking the Haar one as canonical because that agrees with standard geometric calculus)*

### Definite Integral

$$
J^{[a, b]}_{\oplus} [f] = \lim_{N \to \infty} \bigoplus_{n=0}^N [f(x_n) \otimes \mu(x_n, x_{n-1})]
$$

Where the $N$ limit is a normal (not $\oplus$) integer limit, and $x_n$ are a partition of $(a, b)$ which approaches size $0$ and $\mu(dx)$ should approach $0_{\otimes}$. To make life easy, the $x_n$ should be placed so $\mu(dx)$ is a constant (not $\Delta x$). Note that the interval $(a, b)$ is defined totally independently of $\oplus$, but its _length_ is not.

### Indefinite Integral

$$
J_{\oplus} [f](x) = J^{(a, x)}_{\oplus} [f]
$$

(for any fixed $a$; all are correct indefinite integrals)

We have

$$
D_{\oplus} [J^{(a, x)}_{\oplus} [f]] = f
$$

(This property requires that $D$ and $J$ use the same metric $d$, for anyone tracking, which I am since I'm worried there's a weird ambiguity there)

### Taylor Series

This one maybe bears some explaining: the analogue of $\frac{x^n}{n!}$ in additive calculus is not, in general, a polynomial (even in the sense of $\otimes$), so we define them by what we want them to do. I'll call them Taylor functions, $P_{\oplus, n}$.

Defined recursively such that

$$
D_{\oplus} P_{\oplus, 0}(x) = e_{\oplus}
$$

$$
D_{\oplus} P_{\oplus, n}(x) = P_{\oplus, (n - 1)}(x)
$$

$$
TS_{\oplus}(x) = \bigoplus_{n=0}^{\infty} [a_n \otimes P_{\oplus, n}(x)]
$$

*(If we want to do Laurent series, do we need to redefine the complex plane $\mathbb{C}^{\oplus}$ as the algebraic completion of $\mathbb{R}$? I don't feel confident I could investigate this quickly. Maybe they're the same, or both work, or each works but differently.)*

## Some Examples:

### Geometric Calculus

*(I think this has to be restricted to positive numbers, otherwise you end up having $a$ and $-a$ at zero distance from each other, which messes up limits, I think.)*

$$
a \oplus b = a \cdot b
$$

$$
a \otimes b = a^{\ln b}
$$

$$
a \oslash b = a^{\frac{1}{\ln b}}
$$

$$
(-a) = \frac{1}{a}
$$

$$
e_{\oplus} = 1
$$

$$
e_{\otimes} = e
$$

*(RHS is the real regular $e = 2.7\ldots$)*

$$
POS = \{ x \mid |x| > 1 \} 
$$

(note this would be disconnected if we had allowed negatives!)

$$
d\mu(x) = \frac{1}{x}
$$

$$
D_G f = e^{\left( \frac{f'(x)}{f(x)} \right)}
$$

$$
J_G^{(a, b)} f = \exp \left( \int_{(a, b)} \ln f \, dx \right)
$$

$$
P_{G, n}(x) = \exp \left( \frac{x^n}{n!} \right)
$$

### Harmonic Calculus

$$
a \oplus b = \frac{1}{\left( \frac{1}{a} + \frac{1}{b} \right)}
$$

$$
a \otimes b = a b
$$

$$
a \oslash b = \frac{a}{b}
$$

$$
(-a) = -a
$$

$$
e_{\oplus} = \infty
$$

$$
POS = \{ x > 0 \}
$$

$$
d\mu(x) = \frac{1}{x^2}
$$

$$
D_H f = - \frac{f^2(x)}{f'(x)}
$$

$$
J_H f = \frac{1}{\int \frac{dx}{f}}
$$

$$
P_{H, n} = \frac{n!}{x^n}
$$

### Twisted Addition (the most general thing we'll consider)

$$
\oplus = f^{-1}(f(x) + f(y))
$$

$$
\otimes = f^{-1}(f(x) \cdot f(y))
$$

$$
\oslash = f^{-1}\left( \frac{f(x)}{f(y)} \right)
$$

$$
(-a) = f^{-1}(-f(a))
$$

$$
e_{\oplus} = f^{-1}(0)
$$

$$
POS = \{ x \mid f(x) > 0 \}
$$

$$
d\mu(x) = |f'(x)|
$$

*(Note changing the function from $f$ to $g$, so as not to confuse with the transformation function $f$.)*

$$
Dg = f^{-1}[f'(g(x)) \cdot g'(x)]
$$

$$
Jg = f^{-1}\left[ \int f(g(x)) \cdot dx \right]
$$

$$
P_n(x) = f^{-1}\left( \frac{x^n}{n!} \right)
$$

*(Geometric calculus has twisting function $f_G(x) = \ln(x)$ and harmonic calculus has $f_H(x) = \frac{1}{x}$. If you want a laugh, you can also do $f(x) = e^{\alpha x}$, which in the limit $\alpha$ to infinity gives you the 'tropical' calculus)*

## Abstract Functions

Now we have a nice little recipe book of new derivatives and so forth. Here's the really neat part!

So just as in linear algebra, a lot of fuss is made over how a matrix is a mere representation of a particular abstract linear operator with respect to some basis, we can now see that, in some sense, all of this nonlinear calculus is just representing some abstract relationships between functions using particular versions of $\oplus$, $\ominus$, etc. In particular, STOP seeing $\oplus$ as representing a particular operation we do to numbers, like $+$ or harmonic sum, and START seeing it as representing the abstract idea of addition. And likewise for the other operators too.

Put another way, we can abstract away the particular implementation of these operations and talk JUST about the abstract relationships between objects. All the "answers" above, where I spell out e.g., "otimes is actually implemented by $f^{-1}(f(x) \otimes f(y))$", you should actually read as "otimes CAN BE REPRESENTED IN THE STANDARD FIELD as $f^{-1}(f(x) \otimes f(y))$". BUT you could obviously do the opposite and say "REGULAR multiplication can be represented in the $\oplus$ field as $a \otimes b = f(f^{-1}(a) \otimes f^{-1}(b))$".

As an example with functions, if you have some $p_+$, you get $p_{\times}$ by rewriting all the operators in $p_+$ by their $\oplus$ counterparts. E.g., $p_+(x) = x \otimes x \otimes x$, so $p_{\times}(x) = x \otimes x \otimes x = x^{\ln(x)^{\ln(x)}}$. $p_+$ is the representation of $p$ in the standard field, and $p_{\times}$ is the representation of $p$ in the geometric world (the $x^{\dots}$ bit is just a tutorial on how to calculate that).

Cute, right? We can take this further. Consider the arbitrarily selected differential equation

$$
\frac{d}{dx} y + q(x)^2 y = p(x)
$$

More suggestively,

$$
D_+ y_+ + q_+(x)^2 \cdot y_+ = p_+(x)
$$

The plus subscript means "in the standard field."

Obviously, you can tell where I'm going with this;

$$
D_{\oplus} y_{\oplus} \oplus (q_{\oplus}(x) \otimes q_{\oplus}(x)) \otimes y = p_{\oplus}(x)
$$

or less irritatingly:

$$
D y \oplus ((q(x) \otimes q(x)) \otimes y) = p(x)
$$

Now this is an "abstract differential equation"; $p$ and $q$ are 'abstract functions', and $\oplus$ is 'abstract addition'. The ODEs we normally deal with are, in some sense, representing this abstract relationship "in the standard field." Or another perspective is that this is one ODE for each definition of $\oplus$.

The kicker is this: since we can define $e^x$ and $\log x$ and so on via power series, we can solve this ODE in whatever representation we like most, and 'transform back' (by just writing down your answer, and then switching how you interpret the fundamental operations, and then 'unwinding').

### Using this to solve an ODE
Let's try and construct a DE that's hard to solve in the regular representation, but easy in the harmonic one:

We know $D_H g = -\frac{g^2}{g'}$ (i.e., $D_H$ in the standard field representation as opposed to the harmonic one).

So,

$$
D_H D_H g = \frac{g}{g'} (g'' - 2 g')
$$

which looks complicated enough to give something that I would be intimidated by.

So maybe something like

$$
y'' - (p - 2) \frac{y'}{y} = 0
$$

All we have to do is recognize $D_H^2$:

$$
D_H^2 y = p_+(x)
$$

Now we can solve $y'' = p(x)$

$$
y = A x + B + J^{(0, x)}_{\oplus} (J^{(0, x_1)}_{\oplus} [p_H(x_2)])
$$

And now we transform back by reinterpreting:

$$
\frac{1}{y} = \frac{1}{A x} + \frac{1}{B} + \frac{1}{ \int_0^x \frac{dx_1}{ \left[ \int_0^{x_1} \frac{dx_2}{ [p_+(x_2)] } \right] } }
$$

I'm not going to actually verify that that's a solution because I haven't learned to use SymPy yet, lol. *(It's on the list!)* (If it _is_ wrong, the principle I think still stands)

This also means that every ODE you've ever solved is actually also a solution to a whole family of other ODEs too!

In particular, there's what I think is a Lie Group of solutions to other ODEs 'parameterized' by the twisting function $f$ (I have only a schematic idea of what formal requirements would need to be imposed to make this definitely true, presumably smoothness). The action of an element of the group on a ODE or ODE solution would be to transform it into the corresponding representation (Harmonic, Geometric, etc.).

## Relationship to Continued Function Approximations

Let's say we have a continued function approximation of something of interest—i.e., something like $f(a + f(b + f(c + \dots)))$. Or any reasonable variant thereof. We should now be pretty sanguine that we have the ability to re-represent these.

Continued products are a pretty simple example, just because the transformation using $\ln$ is pretty obvious, so let's try continued fractions instead, for flavor!

$$
f(x) = \frac{1}{ \left( \frac{1}{b_1} + \frac{x}{ \left( \frac{1}{b_2} + \frac{x}{ \left( \frac{1}{b_3} + \dots \right) } \right) } \right) }
$$

*(Normally the $b_1$'s are inverted compared to this definition, but I'm tired of trying to close parentheses, thus cheating.)*

This is just

$$
f(x) = b_1 \oplus (x \otimes (b_2 \oplus (x \otimes b_3 \dots)))
$$

or abstractly

$$
f(x) = b_1 + x \otimes (b_2 + x \otimes (\dots))
$$

Which is equivalent to a Taylor series in $x$ (with coefficients $a_n = b_0 b_1 \dots b_n$). How fun!

In general, if we have some continued function approximation, $y = f(a_1 + x f(a_2 + \dots))$, as long as $f$ is invertible, we can do 'twisted addition' with $f$ the twisting function, whereon $y$ is just the same multiply-y version of the Taylor series as above! So, in some sense, most continued-function approximations are also Taylor series!

So now we have an answer to our initial question - Taylor series : derivative :: continued f-approximation : twisted-by-f derivative

Hooray!

## Convergence of Continued Function Approximations

So now I'm gonna fuddle about with some definitions until I get one that makes sense to me for doing calculations:

Suppose we have some _expression_ consisting of strings of variables and/or operations $+, -, \times, \div$ and further assume that this expression has a canonical ordering for any two things getting multiplied—i.e., we're talking regular real numbers, but where you have to 'track' which operand of $\times$ is left vs right, say by replacing $\times$ with a special function $t(a, b)$ which is equal to $t(b, a)$ in value but not 'in expression'. Call this expression $E_1$ (think of it as a list of symbols if that helps). Then let's specify some twisting function $f$, and define:

$$
f * E_1 = E_2 = \{ \text{sym if sym.is\_variable()} \text{ else } \text{convert\_to\_O}(\text{sym}) \}
$$

"For each symbol in the expression, if it's a variable, leave it alone, but if it's an operation, replace it with its $\oplus$ counterpart." *(I'm not worrying about things like handling parentheses, etc., since the extension is obvious.)*

For a given value of variables (I'll call them all 'x', lol), evaluating $E_1(x)$ and $E_2(x)$ will give different numbers. They _are_ related though in that:

$$
[f * E_1](x) = E_2(x) = f^{-1}(E_1(f(x)))
$$

And also:

$$
E_1(x) = f([f * E_1](f^{-1}(x)))
$$

Standard coordinate change stuff, but I always mess it up unless I do it this way, lol.

Consider the general continued function approximation

$$
g(z) = b_0 + z \cdot f(b_1 + z \cdot f(\dots))
$$

Call this expression $G_1(z, \{ b_n \})$.

$g(z)$ is equal at all orders to the series, without arranging terms or anything:

$$
g(z) = f^{-1}(b_0) \oplus f^{-1}(z) \otimes f^{-1}(b_1) \oplus \dots = \bigoplus_{n=0}^{\infty} [f^{-1}(z)^n \otimes f^{-1}(b_n)]
$$

Call this expression $G_2(z, \{ b_n \})$.

Then we see that:

$$
[f^{-1} * G_2](z, \{ b_n \}) = \sum_{n=0}^{\infty} f^{-1}(z)^n b_n
$$

and then:

$$
[f^{-1} * G_2](f(z), \{ b_n \}) = \sum_{n=0}^{\infty} z^n b_n
$$

Cauchy-Hadamard theorem tells us how to find the radius of convergence of the series for this last expression. The second-to-last expression will then converge absolutely for all $ \| f^{-1}(z) \|  < R$, where

$$
R = \frac{1}{\limsup_{n \to \infty} (|f^{-1}(b_n)|^{1/n})}.
$$

Can we use this to say when the formal sequence $G_1$ will converge? Plug in the identity above $ E_1(x) = f\left(\left[f * E_1\right]\left(f^{-1}\left(x\right)\right)\right) $ (“Real Taylor series = $f$ (pseudo-Taylor series with different args)”—they are equal at each step in the sequence).

We know the following: $ \left[ f^{-1} * G_2 \right] \left( z, \{ b_n \} \right) $ converges for $ \| f^{-1} \left( z \right) \| < R$, and that it is equal to the right-hand side of the above in value at every order of partial approximant. Therefore, the sequence of partial approximants (still for a different series than we started with!)

$$
f(G_{2,n}(z, \{ f^{-1}(b_n) \}))
$$

converges if and only if $ \| z \| < R $, to a value we’ll call $ f(L) $.

Assume $f$ is continuous everywhere, so if any sequence $a_n \to a$, then $f(a_n) \to f(a)$. Then the sequence $G_{2,n}(z, \{ f^{-1}(b_n) \})$ converges if and only if $ \| z \| < R$ to $L$ (and thus so does $G_{1,n}(z, \{ f^{-1}(b_n) \})$).

Thus we have:

**Theorem:**

The sequence of continued-function approximants

$$
b_0 + z \cdot f(b_1 + z \cdot f(b_2 + \dots))
$$

converges if $\| z \| < \frac{1}{\limsup_{n \to \infty} (\| f^{-1}(b_n) \|^{1/n})}$, and does not converge if $ \| z \| $ is greater than that; for $z$ equal to $R$, it can converge or diverge. Further, these approximants are equal at each $n$ in the sequence to the $\oplus$ Taylor series:

$$
b_0 + z \cdot f(b_1 + z \cdot f(b_2 + \dots)) = \bigoplus_{n=0}^{\infty} \left[ f^{-1}(z)^n \otimes f^{-1}(b_n) \right]  = f^{-1}\left( \sum_{n=0}^{\infty} b_n f\left( \left[ f^{-1}(z) \right]^n \right) \right).
$$

## Some Ideas That Didn't Make It In
- Variational calculus on twisting function $f$, maybe so that you can linearize some nonlinear ODE? Maybe do a Lie group flow in 'some optimal way' to achieve some objective
- Differential geometry + connection to Lie groups etc. - well beyond my ken for now.
- Eigenvalue equations? Connection to Sturm-Liouville?
- Are there any neat tricks you can use for multivariable equations? Like "transforming one variable but not the other"?
