# Image Descriptions for "Why Differential Entropy Stinks" Blog Post

This document contains detailed descriptions for all images needed in the blog post. Each image should be created as a high-quality vector graphic (SVG preferred) or high-resolution PNG.

## Image 1: "Negative Differential Entropy Example"
**Location:** Introduction section, after the first paragraph about negative entropy
**Purpose:** Visual demonstration of how differential entropy can be negative
**Description:**
- A coordinate system with x-axis labeled "Probability Density" and y-axis labeled "Value"
- Two probability density functions plotted:
  - A very narrow, tall Gaussian centered at x=0.5 (representing a uniform distribution on [0, 1/2])
  - A broader, shorter Gaussian for comparison
- The narrow Gaussian should be so tall that its area is 1, but it's very concentrated
- Include text annotation: "h(X) = -log(2) < 0" pointing to the narrow distribution
- Use contrasting colors (e.g., red for the problematic narrow distribution, blue for the normal one)
- Include a small inset showing the actual uniform distribution on [0, 1/2] as a rectangle

## Image 2: "Condition Number and Information Loss"
**Location:** "Why Entropy is Still Reasonable Sometimes" section
**Purpose:** Illustrate how condition number affects information preservation
**Description:**
- A 2D coordinate system showing input space (left) and output space (right)
- On the left: a small circular region representing input uncertainty
- On the right: two different transformations of this circle:
  - One that maps the circle to a slightly larger circle (well-conditioned transformation)
  - One that maps the circle to a long, thin ellipse (poorly-conditioned transformation)
- Use arrows to show the mapping from input to output
- Include condition number labels: κ ≈ 1 for the good case, κ >> 1 for the bad case
- Add text: "Small input errors → Large output errors" for the poorly-conditioned case
- Use color coding: green for well-conditioned, red for poorly-conditioned

## Image 3: "Discretization and Reference Measures"
**Location:** "The Discrete Limiting Density Approach" section
**Purpose:** Show how different discretizations lead to different entropy measures
**Description:**
- A horizontal line representing a continuous interval [0, 1]
- Three different discretizations shown:
  - Uniform discretization: equal-sized bins
  - Logarithmic discretization: smaller bins near 0, larger near 1
  - Custom discretization: varying bin sizes
- Show probability mass in each bin as rectangles of different heights
- Include entropy calculations for each discretization
- Use different colors for each discretization scheme
- Add arrows showing the limit as bin size → 0
- Include text explaining that the limit depends on the discretization choice

## Image 4: "Conjugate Operation Framework"
**Location:** "Conjugate Unary Operation Formalism" section
**Purpose:** Visualize the f^(-1)(g(f(x))) structure
**Description:**
- A flow diagram with three boxes connected by arrows:
  - Box 1: "X" (input)
  - Box 2: "f(X)" (transformed input)
  - Box 3: "g(f(X))" (operation applied)
  - Box 4: "f^(-1)(g(f(X)))" (final result)
- Show the function f as a transformation (e.g., log for multiplication)
- Show g as the actual operation (e.g., addition)
- Include examples:
  - Addition: f(x) = x, g(x) = x + y
  - Multiplication: f(x) = log(x), g(x) = x + log(y)
- Use different colors for different operations
- Include mathematical notation alongside the boxes

## Image 5: "Irreversibility Ratio Visualization"
**Location:** "Real Irreversibility Measures Many-to-One-ness" section
**Purpose:** Show how intervals change under operations and how this affects information
**Description:**
- Two panels side by side
- Left panel: Original interval [a, b] with uniform spacing of representable numbers
- Right panel: Transformed interval [a', b'] with the same number of representable numbers
- Show how the spacing changes:
  - For multiplication with x > 1: spacing increases, some numbers get "lost"
  - For multiplication with x < 1: spacing decreases, some numbers get "gained"
- Include the irreversibility ratio R = μ([a', b'])/μ([a, b])
- Show bit loss calculation: -log₂(R)
- Use color coding to show which numbers are lost/gained
- Include a small graph showing R vs x for different operations

## Image 6: "Haar Measure and Number Representations"
**Location:** "Haar Measure and Optimal Representations" section
**Purpose:** Compare fixed-point vs floating-point representations
**Description:**
- Two number lines side by side
- Top: Fixed-point representation with uniform spacing
- Bottom: Floating-point representation with logarithmic spacing
- Show how multiplication affects each:
  - Fixed-point: uniform spacing becomes non-uniform
  - Floating-point: logarithmic spacing remains logarithmic
- Include the Haar measure formulas:
  - Addition: μ([a, b]) ∝ b - a
  - Multiplication: μ([a, b]) ∝ log(b/a)
- Use different colors for the spacing patterns
- Include arrows showing the transformation under multiplication
- Add text explaining why floating-point is "natural" for multiplication

## Image 7: "Fixed-Point vs Floating-Point Multiplication"
**Location:** "Concrete Examples" section
**Purpose:** Detailed comparison of precision loss in different representations
**Description:**
- A detailed view of a small interval [1, 2] in both representations
- Show the exact representable numbers in each system
- Demonstrate multiplication by 1.5:
  - Fixed-point: show how some numbers get "squeezed out"
  - Floating-point: show how the spacing pattern is preserved
- Include the irreversibility ratio calculations
- Show bit loss: log₂(1.5) ≈ 0.58 bits for fixed-point
- Use a magnifying glass effect to show the detail
- Include a small table comparing the two approaches

## Image 8: "Vector Operations and Privileged Bases"
**Location:** "Vector Operations and Privileged Bases" section
**Purpose:** Show how coordinate system choice affects irreversibility
**Description:**
- A 2D coordinate system with a vector x = (x₁, x₂)
- Show two different coordinate systems:
  - Standard basis: (1,0), (0,1)
  - Rotated basis: (cos θ, sin θ), (-sin θ, cos θ)
- Demonstrate how the same operation affects the vector differently in each basis
- Show that information loss depends on the choice of basis
- Include the coordinate-wise operation formula
- Use different colors for different bases
- Include arrows showing the transformation in each basis

## Image 9: "Applications and Implications"
**Location:** "Implications and Applications" section
**Purpose:** Overview of practical applications
**Description:**
- A mind map or flowchart showing different application areas:
  - Numerical Algorithms (with examples: matrix multiplication, accumulation)
  - Machine Learning (neural networks, training stability)
  - Information Theory (data processing inequality)
  - Geometric Approaches (Wasserstein distance)
- Connect each application to the main concepts (condition number, Haar measure, etc.)
- Use icons or small diagrams for each application area
- Include key takeaway messages for each area
- Use a hierarchical layout with the main concept in the center

## Image 10: "Summary Framework"
**Location:** Conclusion section
**Purpose:** Visual summary of the three factors affecting irreversibility
**Description:**
- A triangular diagram with three vertices:
  - "Operation" (addition, multiplication, etc.)
  - "Operands" (distribution, scale)
  - "Representation" (fixed-point, floating-point, etc.)
- In the center: "Irreversibility = f(operation, operands, representation)"
- Show examples at each vertex
- Include arrows showing how each factor influences the others
- Use a clean, minimalist design
- Include the key insight about choosing representations that match Haar measures

## Technical Specifications

**Format:** SVG preferred, PNG acceptable at 300 DPI minimum
**Colors:** Use a consistent color scheme throughout:
- Primary: #2E86AB (blue)
- Secondary: #A23B72 (purple)
- Accent: #F18F01 (orange)
- Error/Warning: #C73E1D (red)
- Success: #4CAF50 (green)

**Typography:** Use a clean, readable font (Arial, Helvetica, or similar)
**Size:** All images should be 600-800 pixels wide for web display
**Accessibility:** Ensure sufficient color contrast and include alt text descriptions 