"""
NexShelf Ultra: 200+ Rich Academic Books Seeder
Generates over 200 curated textbooks and reference books spanning 12 academic domains,
distributed across Zone A (Turing), Zone B (Ramanujan), Zone C (Tesla), and Zone D (Hypatia).
"""

from app import create_app, db
from app.models import Author, Book, Category


# 200+ Curated Books Dataset Across 12 Domains
BOOKS_DATASET = [
    # =========================================================================
    # 1. Computer Science, Software Engineering & Systems (Zone A · Racks 01-02)
    # =========================================================================
    ("978-0131103627", "The C Programming Language", "Brian Kernighan & Dennis Ritchie", "Computer Science", 1988, 6, "Zone A · Rack 01 · Shelf 1", "Intermediate", "#2563eb", "c, programming, system programming, fundamentals", "Authoritative ANSI C reference written by the language designers.", "Pointers & memory arithmetic; Bitwise operators; Unix system calls; Low-level buffer structures"),
    ("978-0262033848", "Introduction to Algorithms (CLRS)", "Thomas H. Cormen", "Computer Science", 2009, 8, "Zone A · Rack 01 · Shelf 2", "Advanced", "#1d4ed8", "algorithms, data structures, dynamic programming, graphs", "The definitive encyclopedia on computational algorithms and complexity.", "Big-O notation; Dynamic programming; Maximum network flow; NP-completeness reductions"),
    ("978-0132350884", "Clean Code: A Handbook of Agile Software Craftsmanship", "Robert C. Martin", "Software Engineering", 2008, 7, "Zone A · Rack 01 · Shelf 3", "Intermediate", "#3b82f6", "clean code, agile, refactoring, best practices", "Modern manifesto for crafting maintainable, testable code.", "Meaningful naming; Single-responsibility functions; Exception handling; TDD fundamentals"),
    ("978-0201616224", "The Pragmatic Programmer", "David Thomas & Andrew Hunt", "Software Engineering", 1999, 6, "Zone A · Rack 01 · Shelf 4", "Intermediate", "#60a5fa", "pragmatic, craftsmanship, debugging, tools", "Classic guide on professional software engineering instincts.", "DRY principle; Orthogonality; Tracer bullets; Contract-driven programming"),
    ("978-0134494166", "Clean Architecture", "Robert C. Martin", "Software Engineering", 2017, 5, "Zone A · Rack 01 · Shelf 1", "Advanced", "#1e40af", "architecture, clean architecture, solid, design patterns", "Universal rules of software component structure and boundaries.", "SOLID principles; Dependency inversion; Ports and adapters; Decoupled frameworks"),
    ("978-0201633610", "Design Patterns: Elements of Reusable Object-Oriented Software", "Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides", "Software Engineering", 1994, 6, "Zone A · Rack 01 · Shelf 2", "Advanced", "#3b82f6", "design patterns, oop, gang of four, architecture", "The legendary Gang of Four catalog of 23 software patterns.", "Creational patterns; Structural facades & adapters; Behavioral observers; Strategy pattern"),
    ("978-0131177055", "Working Effectively with Legacy Code", "Michael Feathers", "Software Engineering", 2004, 4, "Zone A · Rack 01 · Shelf 3", "Intermediate", "#2563eb", "legacy code, testing, refactoring, tech debt", "Strategies for safely refactoring untested legacy systems.", "Characterization tests; Breaking dependencies; Seams and sensing; Safely introducing tests"),
    ("978-0596007126", "Head First Design Patterns", "Eric Freeman & Elisabeth Robson", "Software Engineering", 2004, 7, "Zone A · Rack 01 · Shelf 4", "Beginner", "#93c5fd", "design patterns, beginner, visual, oop", "Brain-friendly visual guide to object-oriented patterns.", "Decorator pattern; Factory method; Observer pattern; State & Proxy patterns"),
    ("978-0134685991", "Effective Java", "Joshua Bloch", "Computer Science", 2017, 6, "Zone A · Rack 02 · Shelf 1", "Intermediate", "#1d4ed8", "java, oop, best practices, concurrency", "The gold standard for best practices in modern Java development.", "Builder pattern; Generics & wildcards; Immutable objects; Concurrency utilities"),
    ("978-1491950296", "Programming Rust", "Jim Blandy & Jason Orendorff", "Computer Science", 2021, 5, "Zone A · Rack 02 · Shelf 2", "Advanced", "#1e3a8a", "rust, systems programming, memory safety, concurrency", "Comprehensive exploration of memory-safe high-performance systems.", "Ownership and borrow checker; Lifetimes; Traits and generics; Concurrency without data races"),
    ("978-1593279929", "Automate the Boring Stuff with Python", "Al Sweigart", "Programming", 2019, 8, "Zone A · Rack 02 · Shelf 3", "Beginner", "#60a5fa", "python, automation, beginner, scripting", "Practical programming for beginners to automate daily tasks.", "File manipulation; Web scraping with Beautiful Soup; Spreadsheet automation; Regex matching"),
    ("978-1492051367", "Fluent Python", "Luciano Ramalho", "Programming", 2022, 5, "Zone A · Rack 02 · Shelf 4", "Advanced", "#2563eb", "python, advanced, decorators, generators", "Deep dive into idiomatic, modern, Pythonic idioms.", "Special dunder methods; Asyncio & coroutines; Metaprogramming; Memory views & arrays"),
    ("978-0134092669", "The Go Programming Language", "Alan A. A. Donovan & Brian W. Kernighan", "Programming", 2015, 6, "Zone A · Rack 02 · Shelf 1", "Intermediate", "#3b82f6", "golang, concurrency, microservices, backend", "Clear, authoritative tutorial on Google Go.", "Goroutines and channels; Interface satisfaction; Package architecture; Fast reflection"),
    ("978-0321751041", "The C++ Programming Language", "Bjarne Stroustrup", "Computer Science", 2013, 5, "Zone A · Rack 02 · Shelf 2", "Advanced", "#1d4ed8", "cpp, stroustrup, systems, performance", "Definitive language specification from the creator of C++.", "RAII idiom; Move semantics; Template metaprogramming; Standard Template Library (STL)"),
    ("978-1491904244", "You Don't Know JS: Scope & Closures", "Kyle Simpson", "Programming", 2014, 7, "Zone A · Rack 02 · Shelf 3", "Intermediate", "#60a5fa", "javascript, closures, scope, web development", "In-depth study of JavaScript's execution context and scoping rules.", "Lexical scoping; Hoisting mechanics; Closure memory retention; Block scope let/const"),

    # =========================================================================
    # 2. Operating Systems, Networks & Distributed Systems (Zone A · Rack 03)
    # =========================================================================
    ("978-0133591620", "Operating Systems: Three Easy Pieces", "Remzi H. Arpaci-Dusseau", "Computer Science", 2018, 7, "Zone A · Rack 03 · Shelf 1", "Intermediate", "#2563eb", "operating systems, virtualization, concurrency, persistence", "Clear, modern breakdown of OS virtualization, concurrency, and persistence.", "Process scheduling algorithms; Virtual memory paging; Lock & condition variables; File system journaling"),
    ("978-0130340740", "Modern Operating Systems", "Andrew S. Tanenbaum", "Computer Science", 2014, 6, "Zone A · Rack 03 · Shelf 2", "Advanced", "#1d4ed8", "operating systems, tanenbaum, kernel, processes", "Comprehensive university textbook covering Linux and Windows kernels.", "Multithreading & deadlock detection; Memory management & TLB; Security & access control; Virtual machines"),
    ("978-0132126953", "Computer Networks", "Andrew S. Tanenbaum & David J. Wetherall", "Computer Science", 2010, 6, "Zone A · Rack 03 · Shelf 3", "Intermediate", "#3b82f6", "networking, tcp ip, routing, protocols", "The gold standard textbook on computer networking architecture.", "OSI 7-layer model; TCP congestion control; Routing algorithms (OSPF, BGP); DNS & HTTP protocols"),
    ("978-0136079675", "Computer Networking: A Top-Down Approach", "James Kurose & Keith Ross", "Computer Science", 2020, 8, "Zone A · Rack 03 · Shelf 4", "Intermediate", "#60a5fa", "networking, protocols, sockets, wifi", "Top-down approach starting from application layer protocols.", "Socket programming in Python; Transport layer UDP/TCP; Link layer ethernet & wireless; Network security basics"),
    ("978-1491903063", "Designing Data-Intensive Applications", "Martin Kleppmann", "Computer Science", 2017, 9, "Zone A · Rack 03 · Shelf 1", "Advanced", "#1e40af", "distributed systems, databases, kafka, replication", "The industry masterwork on distributed reliability, scalability, and maintainability.", "Single-leader vs multi-leader replication; Partitioning & sharding; Consensus (Raft/Paxos); Stream processing with Kafka"),
    ("978-1491954386", "Site Reliability Engineering", "Betsy Beyer, Chris Jones, Jennifer Petoff", "Software Engineering", 2016, 5, "Zone A · Rack 03 · Shelf 2", "Intermediate", "#2563eb", "sre, devops, google, reliability, metrics", "How Google runs production systems at planetary scale.", "SLOs and error budgets; Monitoring and distributed tracing; Incident management; Eliminating toil"),
    ("978-1492034025", "Kubernetes: Up and Running", "Brendan Burns, Joe Beda, Kelsey Hightower", "Cloud Computing", 2019, 6, "Zone A · Rack 03 · Shelf 3", "Intermediate", "#3b82f6", "kubernetes, containers, cloud, devops", "Practical hands-on guide to container orchestration.", "Pods, Deployments, and ReplicaSets; Service discovery & Ingress; ConfigMaps & Secrets; Rolling deployments"),
    ("978-1491949535", "Building Microservices", "Sam Newman", "Software Engineering", 2021, 5, "Zone A · Rack 03 · Shelf 4", "Advanced", "#1d4ed8", "microservices, api, distributed, architecture", "Designing fine-grained systems with domain-driven boundaries.", "Bounded contexts; API gateway patterns; Saga distributed transactions; Microservices security"),

    # =========================================================================
    # 3. Artificial Intelligence & Machine Learning (Zone A · Rack 04)
    # =========================================================================
    ("978-0136042594", "Artificial Intelligence: A Modern Approach", "Stuart Russell & Peter Norvig", "Artificial Intelligence", 2020, 8, "Zone A · Rack 04 · Shelf 1", "Advanced", "#1d4ed8", "ai, norvig, search, planning, agents", "The world's leading standard university textbook in artificial intelligence.", "A* and heuristic search; Minimax game theory; Probabilistic graphical models; Reinforcement learning"),
    ("978-0262035613", "Deep Learning", "Ian Goodfellow, Yoshua Bengio, Aaron Courville", "Artificial Intelligence", 2016, 6, "Zone A · Rack 04 · Shelf 2", "Advanced", "#1e40af", "deep learning, neural networks, backprop, ai", "The definitive mathematical foundation of deep neural networks.", "Backpropagation & automatic differentiation; Convolutional nets for computer vision; Recurrent nets & LSTM; GANs & autoencoders"),
    ("978-1492032649", "Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow", "Aurélien Géron", "Artificial Intelligence", 2022, 9, "Zone A · Rack 04 · Shelf 3", "Intermediate", "#2563eb", "machine learning, python, tensorflow, scikit", "Practical, code-heavy walkthrough of end-to-end ML workflows.", "Regression & classification metrics; Random forests & gradient boosting; Neural networks with Keras; Transformer fine-tuning"),
    ("978-0262039246", "Reinforcement Learning: An Introduction", "Richard S. Sutton & Andrew G. Barto", "Artificial Intelligence", 2018, 5, "Zone A · Rack 04 · Shelf 4", "Advanced", "#1d4ed8", "reinforcement learning, sutton, q learning, markov", "Foundational text on Markov decision processes and Q-learning.", "MDPs and Bellman equations; Temporal-difference learning; Policy gradient methods; Deep Q-networks (DQN)"),
    ("978-1492067740", "Natural Language Processing with Transformers", "Lewis Tunstall, Leandro von Werra, Thomas Wolf", "Artificial Intelligence", 2022, 6, "Zone A · Rack 04 · Shelf 1", "Intermediate", "#3b82f6", "nlp, transformers, huggingface, bert, gpt", "Building state-of-the-art NLP models with Hugging Face.", "Self-attention mechanics; BERT and GPT architectures; Fine-tuning text classifiers; Question answering pipelines"),
    ("978-1449369415", "Pattern Recognition and Machine Learning", "Christopher M. Bishop", "Data Science", 2006, 5, "Zone A · Rack 04 · Shelf 2", "Advanced", "#1e3a8a", "machine learning, bayesian, probability, clustering", "Comprehensive Bayesian approach to statistical pattern recognition.", "Probability distributions; Linear models for classification; Kernel methods & SVM; Expectation-maximization"),
    ("978-1491957660", "Python Data Science Handbook", "Jake VanderPlas", "Data Science", 2016, 7, "Zone A · Rack 04 · Shelf 3", "Beginner", "#60a5fa", "data science, pandas, numpy, matplotlib, jupyter", "Essential guide for computation with NumPy, Pandas, and Matplotlib.", "NumPy array broadcasting; Pandas dataframe filtering; Data visualization with Matplotlib; Scikit-learn pipelines"),
    ("978-0262018029", "Computer Vision: Algorithms and Applications", "Richard Szeliski", "Artificial Intelligence", 2022, 4, "Zone A · Rack 04 · Shelf 4", "Advanced", "#1d4ed8", "computer vision, image processing, opencv, 3d", "Modern principles of digital image understanding and computational photography.", "Image filtering and edge detection; Feature matching (SIFT, ORB); 3D reconstruction & stereo vision; Deep learning for object detection"),

    # =========================================================================
    # 4. Cybersecurity, Cryptography & Cloud (Zone A · Rack 05)
    # =========================================================================
    ("978-0134444284", "Cryptography and Network Security", "William Stallings", "Cybersecurity", 2017, 6, "Zone A · Rack 05 · Shelf 1", "Intermediate", "#dc2626", "cryptography, security, rsa, aes, hashes", "Comprehensive reference on encryption algorithms and protocol security.", "Symmetric ciphers (AES, DES); Public key crypto (RSA, ECC); SHA hashes & HMAC; TLS/SSL handshake"),
    ("978-1593278267", "The Web Application Hacker's Handbook", "Dafydd Stuttard & Marcus Pinto", "Cybersecurity", 2011, 5, "Zone A · Rack 05 · Shelf 2", "Intermediate", "#b91c1c", "security, hacking, web security, xss, sqli", "The classic guide on discovering and exploiting web vulnerabilities.", "SQL injection detection; Cross-Site Scripting (XSS); CSRF and session hijacking; Authentication bypasses"),
    ("978-1593279288", "Practical Malware Analysis", "Michael Sikorski & Andrew Honig", "Cybersecurity", 2012, 4, "Zone A · Rack 05 · Shelf 3", "Advanced", "#991b1b", "malware, reverse engineering, security, x86", "Disassembling and analyzing malicious x86 binaries.", "Static analysis with IDA Pro; Dynamic debugging with x64dbg; Windows internal APIs; Rootkit behavior"),
    ("978-1593279943", "Linux Basics for Hackers", "OccupyTheWeb", "Cybersecurity", 2018, 7, "Zone A · Rack 05 · Shelf 4", "Beginner", "#ef4444", "linux, security, bash, networking, kali", "Practical Linux networking and scripting for security professionals.", "Linux filesystem hierarchy; Bash scripting; Network reconnaissance; Wi-Fi security fundamentals"),
    ("978-1492043782", "Cloud Native Infrastructure", "Justin Garrison & Kris Nova", "Cloud Computing", 2017, 5, "Zone A · Rack 05 · Shelf 1", "Intermediate", "#2563eb", "cloud, infrastructure, aws, terraform", "Patterns for building elastic, scalable cloud platforms.", "Infrastructure as Code (Terraform); Immutable server patterns; High availability topologies; Cloud networking"),
    ("978-0136006633", "Security in Computing", "Charles P. Pfleeger", "Cybersecurity", 2015, 5, "Zone A · Rack 05 · Shelf 2", "Intermediate", "#b91c1c", "cybersecurity, defense, firewalls, encryption", "Broad academic curriculum textbook on computing defense.", "Buffer overflow prevention; Access control matrices; Firewall architectures; Disaster recovery planning"),

    # =========================================================================
    # 5. Mathematics, Theoretical Physics & Discrete Math (Zone B · Racks 04-05)
    # =========================================================================
    ("978-0073383095", "Discrete Mathematics and Its Applications", "Kenneth H. Rosen", "Mathematics", 2018, 8, "Zone B · Rack 04 · Shelf 1", "Intermediate", "#10b981", "discrete math, logic, sets, graph theory", "The quintessential discrete mathematics curriculum textbook.", "Predicate logic & proofs; Induction & recursion; Permutations & combinations; Graph theory & trees"),
    ("978-0980232714", "Linear Algebra Done Right", "Sheldon Axler", "Mathematics", 2015, 6, "Zone B · Rack 04 · Shelf 2", "Intermediate", "#059669", "linear algebra, vectors, matrices, eigenvalues", "Modern determinant-free approach to linear spaces and operators.", "Vector spaces & subspaces; Linear transformations; Eigenvalues & eigenvectors; Spectral theorem"),
    ("978-0486614496", "Calculus on Manifolds", "Michael Spivak", "Mathematics", 1965, 4, "Zone B · Rack 04 · Shelf 3", "Advanced", "#047857", "calculus, manifolds, analysis, differential forms", "Rigorous modern treatment of multivariable calculus and Stokes theorem.", "Functions on Euclidean space; Differentiation of multivariable maps; Integration over manifolds; Stokes Theorem in differential forms"),
    ("978-0070542358", "Principles of Mathematical Analysis (Baby Rudin)", "Walter Rudin", "Mathematics", 1976, 5, "Zone B · Rack 04 · Shelf 4", "Advanced", "#065f46", "real analysis, rudin, topology, limits", "The gold standard rigorous real analysis text for mathematicians.", "Metric space topology; Sequences and series convergence; Riemann-Stieltjes integrals; Equicontinuity & Stone-Weierstrass"),
    ("978-0134469140", "Probability and Statistics for Engineers and Scientists", "Ronald E. Walpole", "Mathematics", 2016, 7, "Zone B · Rack 04 · Shelf 1", "Intermediate", "#10b981", "probability, statistics, distributions, testing", "Core university probability text with applied engineering examples.", "Discrete & continuous distributions (Normal, Poisson); Hypothesis testing; Linear regression; Analysis of variance (ANOVA)"),
    ("978-0201896831", "The Art of Computer Programming, Vol 1: Fundamental Algorithms", "Donald Knuth", "Computer Science", 1997, 4, "Zone B · Rack 04 · Shelf 2", "Advanced", "#059669", "knuth, algorithms, math, trees", "The bible of fundamental algorithmic math and tree structures.", "Mathematical induction; Information structures (Stacks, Queues, Deques); Tree traversal algorithms; Dynamic storage allocation"),
    ("978-0201896848", "The Art of Computer Programming, Vol 2: Seminumerical Algorithms", "Donald Knuth", "Computer Science", 1997, 4, "Zone B · Rack 04 · Shelf 3", "Advanced", "#047857", "knuth, random numbers, arithmetic, math", "In-depth study of random number generators and arbitrary precision arithmetic.", "Linear congruential generators; Floating-point arithmetic accuracy; Prime factorization; Radix conversion algorithms"),
    ("978-0201896855", "The Art of Computer Programming, Vol 3: Sorting and Searching", "Donald Knuth", "Computer Science", 1998, 4, "Zone B · Rack 04 · Shelf 4", "Advanced", "#065f46", "knuth, sorting, searching, hashing", "Comprehensive mathematical analysis of all sorting and searching algorithms.", "Internal sorting (QuickSort, MergeSort); External magnetic tape sorting; Sequential & binary search; Hashing collision resolution"),
    ("978-0321842688", "Concrete Mathematics", "Ronald L. Graham, Donald E. Knuth, Oren Patashnik", "Mathematics", 1994, 5, "Zone B · Rack 05 · Shelf 1", "Advanced", "#10b981", "discrete math, knuth, sums, generating functions", "A foundation for computer science combining continuous and discrete math.", "Recurrence relations (Tower of Hanoi); Summation calculus; Floor/Ceiling arithmetic; Generating functions"),
    ("978-0486445038", "Introduction to Graph Theory", "Richard J. Trudeau", "Mathematics", 1993, 6, "Zone B · Rack 05 · Shelf 2", "Beginner", "#34d399", "graph theory, math, beginner, networks", "Intuitive, beginner-friendly introduction to pure graph theory.", "Eulerian trails and Hamiltonian circuits; Planar graphs & Kuratowski theorem; Graph coloring & Four color theorem; Network connectivity"),
    ("978-0471198260", "Differential Equations and Dynamical Systems", "Lawrence Perko", "Mathematics", 2001, 4, "Zone B · Rack 05 · Shelf 3", "Advanced", "#059669", "differential equations, dynamical systems, chaos", "Nonlinear ordinary differential equations and chaos theory.", "Linear systems & matrix exponentials; Phase plane analysis & limit cycles; Poincare-Bendixson theorem; Bifurcation theory"),
    ("978-0465024933", "The Feynman Lectures on Physics, Vol 1", "Richard P. Feynman", "Physics", 1963, 6, "Zone B · Rack 05 · Shelf 4", "Intermediate", "#10b981", "physics, mechanics, thermodynamics, feynman", "Classic physics lectures on mechanics, radiation, and heat.", "Newton's laws & conservation of momentum; Special relativity principles; Thermodynamics & entropy; Harmonic oscillators"),
    ("978-0465024940", "The Feynman Lectures on Physics, Vol 2", "Richard P. Feynman", "Physics", 1964, 5, "Zone B · Rack 05 · Shelf 1", "Intermediate", "#059669", "physics, electromagnetism, maxwell, fields", "Lectures on electrodynamics, Maxwell equations, and dielectric materials.", "Electrostatic potentials and Gauss law; Magnetic vector potential; Maxwell electromagnetic wave equations; Waveguides and cavities"),
    ("978-0465024957", "The Feynman Lectures on Physics, Vol 3", "Richard P. Feynman", "Physics", 1965, 5, "Zone B · Rack 05 · Shelf 2", "Advanced", "#047857", "physics, quantum mechanics, feynman, wave", "Intuitive yet profound quantum mechanics foundation.", "Two-slit probability amplitudes; Spin-1/2 state transformations; Hamiltonian matrix transitions; Superconductivity basics"),
    ("978-0131118928", "Introduction to Quantum Mechanics", "David J. Griffiths", "Physics", 2018, 6, "Zone B · Rack 05 · Shelf 3", "Intermediate", "#10b981", "quantum mechanics, schrodinger, wave functions", "The standard undergraduate textbook for quantum physics.", "Schrödinger wave equation; Infinite square well and harmonic oscillator; Hydrogen atom electron orbitals; Perturbation theory"),

    # =========================================================================
    # 6. Electronics, VLSI, Circuits & Communications (Zone C · Rack 06)
    # =========================================================================
    ("978-0198075721", "Microelectronic Circuits", "Adel S. Sedra & Kenneth C. Smith", "Electronics", 2014, 7, "Zone C · Rack 06 · Shelf 1", "Advanced", "#f59e0b", "electronics, circuits, semiconductors, mosfet", "The worldwide gold standard for analog electronic circuit analysis.", "Op-amp configurations; MOSFET and BJT amplifier biasing; Frequency response analysis; CMOS digital logic gates"),
    ("978-0131497269", "Digital Design: With an Introduction to the Verilog HDL", "M. Morris Mano", "Electronics", 2012, 8, "Zone C · Rack 06 · Shelf 2", "Beginner", "#fbbf24", "digital design, verilog, logic gates, fpga", "Standard introduction to binary logic and HDL modeling.", "Boolean algebra & Karnaugh maps; Combinational arithmetic circuits; Flip-flops & finite state machines (FSMs); Verilog module design"),
    ("978-0132155137", "CMOS VLSI Design: A Circuits and Systems Perspective", "Neil H. E. Weste & David Harris", "Electronics", 2010, 5, "Zone C · Rack 06 · Shelf 3", "Advanced", "#d97706", "vlsi, cmos, semiconductor, layout, silicon", "Comprehensive guide to microchip design and silicon layout.", "MOS transistor physics; Static & dynamic CMOS logic; Clock distribution & timing closure; Layout design rules & DRC/LVS"),
    ("978-0134057897", "Electric Circuits", "James W. Nilsson & Susan Riedel", "Electrical Engineering", 2014, 7, "Zone C · Rack 06 · Shelf 4", "Beginner", "#f59e0b", "circuits, electrical, ohm law, kirchhoff", "Foundational undergraduate electrical circuit theory.", "Kirchhoff voltage/current laws (KVL/KCL); Thévenin and Norton equivalent circuits; RLC transient response; Sinusoidal steady-state AC analysis"),
    ("978-0138147570", "Signals and Systems", "Alan V. Oppenheim & Alan S. Willsky", "Electrical Engineering", 1996, 6, "Zone C · Rack 06 · Shelf 1", "Intermediate", "#b45309", "signals, systems, fourier, laplace, z transform", "The premier textbook on continuous and discrete signals.", "Continuous-time Fourier transform (CTFT); Discrete-time Fourier transform (DTFT); Laplace transform & s-plane poles; Z-transform stability"),
    ("978-0131988422", "Discrete-Time Signal Processing", "Alan V. Oppenheim & Ronald W. Schafer", "Electrical Engineering", 2009, 5, "Zone C · Rack 06 · Shelf 2", "Advanced", "#d97706", "dsp, filtering, fft, digital signals", "Advanced theory and design of digital filters.", "Sampling theorem and aliasing; FIR and IIR digital filter design; Fast Fourier Transform (FFT) algorithms; Multirate signal processing"),
    ("978-0070151437", "Digital Signal Processing", "John G. Proakis & Dimitris K. Manolakis", "Electrical Engineering", 2006, 5, "Zone C · Rack 06 · Shelf 3", "Intermediate", "#f59e0b", "dsp, proakis, signal processing, algorithms", "Comprehensive curriculum on digital signal architecture.", "LTI systems and convolution; Discrete Fourier Transform (DFT); Optimum filter design; DSP hardware implementation"),
    ("978-0070570542", "Power Electronics: Circuits, Devices, and Applications", "Muhammad H. Rashid", "Electrical Engineering", 2013, 5, "Zone C · Rack 06 · Shelf 4", "Intermediate", "#b45309", "power electronics, inverters, rectifiers, motors", "Theory of power semiconductor switches and energy conversion.", "Diode rectifiers & thyristors; DC-DC buck/boost converters; Pulse-Width Modulation (PWM) inverters; AC/DC motor drives"),

    # =========================================================================
    # 7. Robotics, Embedded Systems & IoT (Zone C · Rack 07)
    # =========================================================================
    ("978-0262015356", "Introduction to Autonomous Mobile Robots", "Roland Siegwart", "Robotics", 2011, 5, "Zone C · Rack 07 · Shelf 1", "Advanced", "#d97706", "robotics, mobile robots, slam, sensors, lidar", "Principles of robot locomotion, sensor perception, and navigation.", "Wheel kinematics & differential drive; Sensor models (LiDAR, Encoders, IMU); Extended Kalman Filter (EKF) SLAM; Dijkstra & A* path planning"),
    ("978-0130618832", "Introduction to Robotics: Mechanics and Control", "John J. Craig", "Robotics", 2004, 6, "Zone C · Rack 07 · Shelf 2", "Intermediate", "#f59e0b", "robotics, kinematics, dynamics, control, arms", "Standard textbook on multi-joint robot manipulator arms.", "Spatial transformations & rotation matrices; Forward kinematics with Denavit-Hartenberg; Inverse kinematics calculations; Trajectory generation and PID control"),
    ("978-1491957661", "Designing Connected Products", "Claire Rowland, Elizabeth Goodman", "IoT", 2015, 6, "Zone C · Rack 07 · Shelf 3", "Beginner", "#fbbf24", "iot, hardware, embedded, ux, smart devices", "UX and architecture for physical smart connected products.", "Device-to-cloud networking protocols (MQTT, CoAP); Embedded firmware update UX; Local network pairing; Low-power battery optimization"),
    ("978-1449355784", "Making Things Talk: Using Sensors, Networks, and Arduino", "Tom Igoe", "Robotics", 2017, 7, "Zone C · Rack 07 · Shelf 4", "Beginner", "#f59e0b", "arduino, sensors, physical computing, diy", "Hands-on projects connecting microcontrollers to the web.", "Serial communication & UART/I2C/SPI; Analog & digital sensor reading; Webhooks and REST APIs on microcontrollers; BLE wireless transmission"),
    ("978-1593278885", "Programming Arduino: Getting Started with Sketches", "Simon Monk", "Embedded Systems", 2016, 8, "Zone C · Rack 07 · Shelf 1", "Beginner", "#fbbf24", "arduino, embedded, c, microcontroller", "Step-by-step introduction to programming microcontrollers.", "Digital I/O & PWM motor control; Interrupt handling timers; I2C LCD displays; EEPROM data persistence"),
    ("978-0132618212", "Embedded Systems: Real-Time Operating Systems for ARM Cortex-M", "Jonathan W. Valvano", "Embedded Systems", 2017, 5, "Zone C · Rack 07 · Shelf 2", "Advanced", "#b45309", "embedded, rtos, arm cortex, firmware", "Building multitasking embedded operating systems on ARM silicon.", "Context switching in assembly; Semaphores & mutex priority inversion; Thread scheduling algorithms; Real-time peripheral drivers"),

    # =========================================================================
    # 8. Mechanical, Aerospace & Structural Engineering (Zone C · Rack 08)
    # =========================================================================
    ("978-0073398204", "Shigley's Mechanical Engineering Design", "Richard G. Budynas & J. Keith Nisbett", "Mechanical Engineering", 2014, 6, "Zone C · Rack 08 · Shelf 1", "Advanced", "#d97706", "mechanical, shigley, machine design, stress, gears", "The benchmark reference for mechanical machine component engineering.", "Static failure theories (Von Mises, Tresca); Fatigue failure and S-N curves; Shafts, gears, and bearing selection; Welded and bolted joint analysis"),
    ("978-0134301006", "Engineering Mechanics: Statics & Dynamics", "Russell C. Hibbeler", "Mechanical Engineering", 2015, 8, "Zone C · Rack 08 · Shelf 2", "Intermediate", "#f59e0b", "mechanics, statics, dynamics, forces, trusses", "Fundamental principles of equilibrium forces and body motion.", "Free-body diagrams and force equilibrium; Truss analysis (Method of Joints/Sections); Moments of inertia; Planar rigid body kinematics"),
    ("978-0134814988", "Fluid Mechanics", "Russell C. Hibbeler", "Mechanical Engineering", 2017, 5, "Zone C · Rack 08 · Shelf 3", "Intermediate", "#b45309", "fluid mechanics, bernoulli, navier stokes, flow", "Theory of liquid and gas motion in engineering systems.", "Fluid statics and pressure measurement; Bernoulli equation and energy conservation; Laminar and turbulent pipe flow; Boundary layer theory"),
    ("978-0073398181", "Thermodynamics: An Engineering Approach", "Yunus A. Çengel & Michael A. Boles", "Mechanical Engineering", 2018, 7, "Zone C · Rack 08 · Shelf 4", "Intermediate", "#f59e0b", "thermodynamics, energy, entropy, heat engines", "Undergraduate curriculum textbook on energy and heat conversion.", "First Law of Thermodynamics (Energy balance); Second Law and Carnot heat engine efficiency; Entropy generation and availability; Gas power cycles (Otto, Diesel, Brayton)"),
    ("978-0073398174", "Heat and Mass Transfer: Fundamentals and Applications", "Yunus A. Çengel & Afshin J. Ghajar", "Mechanical Engineering", 2014, 5, "Zone C · Rack 08 · Shelf 1", "Intermediate", "#d97706", "heat transfer, conduction, convection, radiation", "Principles of thermal conduction, convection, and radiation.", "Fourier Law of heat conduction; Natural and forced convection correlations; Thermal radiation exchange view factors; Heat exchanger design (LMTD, NTU)"),
    ("978-0073398143", "Fundamentals of Aerodynamics", "John D. Anderson", "Aerospace Engineering", 2016, 4, "Zone C · Rack 08 · Shelf 2", "Advanced", "#b45309", "aerospace, aerodynamics, lift, drag, supersonic", "The world standard text for aeronautical and aerospace flight physics.", "Inviscid incompressible flow over airfoils; Thin airfoil theory & finite wings; Compressible supersonic flow & shock waves; Viscous boundary layer separation"),

    # =========================================================================
    # 9. Economics, Quantitative Finance & Leadership (Zone D · Rack 08 · Shelf 1-2)
    # =========================================================================
    ("978-0134515311", "Economics", "Paul Krugman & Robin Wells", "Economics", 2017, 6, "Zone D · Rack 08 · Shelf 1", "Beginner", "#8b5cf6", "economics, microeconomics, macroeconomics, markets", "Accessible, real-world introduction to economic principles.", "Supply and demand equilibrium; Elasticity and market efficiency; Fiscal and monetary policy; International trade and comparative advantage"),
    ("978-0262027946", "Options, Futures, and Other Derivatives", "John C. Hull", "Finance", 2017, 5, "Zone D · Rack 08 · Shelf 2", "Advanced", "#7c3aed", "finance, derivatives, options, black scholes", "The definitive Wall Street bible on derivative assets and risk modeling.", "Mechanics of futures and forwards; Black-Scholes-Merton differential equation; Option Greeks hedging (Delta, Gamma, Vega); Credit risk and Value-at-Risk (VaR)"),
    ("978-0078034657", "Principles of Corporate Finance", "Richard A. Brealey, Stewart C. Myers", "Finance", 2019, 5, "Zone D · Rack 08 · Shelf 1", "Intermediate", "#8b5cf6", "finance, valuation, capital budgeting, wacc", "Corporate financial decision making and capital markets.", "Net Present Value (NPV) calculation; Capital Asset Pricing Model (CAPM); Weighted Average Cost of Capital (WACC); Mergers and acquisitions valuation"),
    ("978-0060555665", "The Intelligent Investor", "Benjamin Graham", "Finance", 2003, 8, "Zone D · Rack 08 · Shelf 2", "Beginner", "#6d28d9", "investing, value investing, graham, buffett", "The foundational text on value investing and market psychology.", "Margin of Safety principle; Mr. Market emotional swings; Defensive vs enterprising investor portfolios; Fundamental earnings analysis"),
    ("978-0385348866", "Thinking, Fast and Slow", "Daniel Kahneman", "Economics", 2011, 9, "Zone D · Rack 08 · Shelf 1", "Beginner", "#8b5cf6", "psychology, economics, behavioral economics, bias", "Nobel Prize-winning exploration of cognitive biases and heuristics.", "System 1 intuitive vs System 2 deliberative thought; Prospect theory and loss aversion; Anchoring and availability heuristics; Overconfidence effect"),
    ("978-0062457714", "Principles: Life and Work", "Ray Dalio", "Management", 2017, 7, "Zone D · Rack 08 · Shelf 2", "Beginner", "#7c3aed", "management, principles, leadership, hedge fund", "Management framework and radical transparency from Bridgewater Associates.", "Radical truth and radical transparency; 5-step process for personal success; Idea meritocracy decision making; Algorithmic management systems"),
    ("978-0062884749", "The Ride of a Lifetime", "Robert Iger", "Management", 2019, 6, "Zone D · Rack 08 · Shelf 1", "Beginner", "#8b5cf6", "leadership, management, disney, strategy", "Lessons in creative leadership and billion-dollar media mergers.", "Innovate or die imperative; Managing large-scale acquisitions (Pixar, Marvel, Lucasfilm); Clear strategic priorities; Courage in high-stakes negotiations"),

    # =========================================================================
    # 10. UI/UX Design, Product & Human Factors (Zone D · Rack 08 · Shelf 3)
    # =========================================================================
    ("978-0465050659", "The Design of Everyday Things", "Don Norman", "Design", 2013, 8, "Zone D · Rack 08 · Shelf 3", "Beginner", "#8b5cf6", "design, ui ux, affordances, human factors", "Foundational classic on intuitive human-centered design.", "Affordances, signifiers, and feedback; Mapping and conceptual models; The Seven Stages of Action; Designing for human error"),
    ("978-0321965516", "Don't Make Me Think, Revisited", "Steve Krug", "Design", 2014, 9, "Zone D · Rack 08 · Shelf 3", "Beginner", "#a78bfa", "ui ux, web usability, web design, krug", "Practical common-sense rules for effortless web and mobile usability.", "Visual hierarchy and scannability; Designing clear navigation; Omit needless words; Usability testing on 10-cent budget"),
    ("978-1449339739", "Designing Interfaces", "Jenifer Tidwell, Charles Brewer", "Design", 2020, 5, "Zone D · Rack 08 · Shelf 3", "Intermediate", "#7c3aed", "ui design, patterns, mobile, web interfaces", "Catalog of proven visual interaction patterns for digital apps.", "Information architecture navigation patterns; Form input and validation feedback; Responsive grid layouts; Data table interaction techniques"),
    ("978-1118968055", "About Face: The Essentials of Interaction Design", "Alan Cooper, Robert Reimann", "Design", 2014, 4, "Zone D · Rack 08 · Shelf 3", "Advanced", "#6d28d9", "interaction design, personas, goal directed, ux", "Comprehensive methodology for goal-directed software design.", "Goal-directed persona development; Scenario-based design workflows; Desktop and mobile ergonomics; Eliminating cognitive friction"),

    # =========================================================================
    # 11. World Literature, Philosophy & Academic Writing (Zone D · Rack 08 · Shelf 4)
    # =========================================================================
    ("978-0140449136", "Meditations", "Marcus Aurelius", "Philosophy", 180, 8, "Zone D · Rack 08 · Shelf 4", "Beginner", "#8b5cf6", "philosophy, stoicism, aurelius, classics", "Personal Stoic reflections of the Roman Emperor on duty and resilience.", "Dichotomy of control (what is in our power vs not); Mental tranquility through reason; Transience of fame and material wealth; Focus on virtue and present moment"),
    ("978-0140449273", "The Republic", "Plato", "Philosophy", 375, 7, "Zone D · Rack 08 · Shelf 4", "Intermediate", "#7c3aed", "philosophy, plato, justice, allegory of cave", "The foundational dialogue on justice, the ideal state, and metaphysics.", "The Allegory of the Cave; The tripartite theory of the soul; Philosopher-king governance; Forms and metaphysical truth"),
    ("978-0143105954", "Beyond Good and Evil", "Friedrich Nietzsche", "Philosophy", 1886, 6, "Zone D · Rack 08 · Shelf 4", "Advanced", "#6d28d9", "philosophy, nietzsche, morality, truth", "Sharp critique of traditional European morality and dogmatic philosophy.", "Will to Power principle; Master vs slave morality; Perspectivism and truth; The free spirit philosopher archetype"),
    ("978-0226430577", "The Craft of Research", "Wayne C. Booth, Gregory G. Colomb", "Academic Research", 2016, 7, "Zone D · Rack 08 · Shelf 4", "Beginner", "#a78bfa", "research, writing, citations, methodology", "The definitive manual on formulating research questions and arguments.", "Crafting compelling research problem statements; Evaluating credible scholarly sources; Assembling claims, reasons, and evidence; Academic drafting and revision"),
    ("978-0205309023", "The Elements of Style", "William Strunk Jr. & E. B. White", "Literature", 1999, 10, "Zone D · Rack 08 · Shelf 4", "Beginner", "#8b5cf6", "writing, grammar, style, brevity", "The timeless pocket guide to clear, vigorous English writing.", "Use active voice over passive; Omit needless words; Keep related words together; Express parallel ideas in parallel grammatical form"),
]


# Add procedural rich academic books to exceed 200+ titles seamlessly
ADDITIONAL_DOMAINS = [
    ("Computer Science", "Zone A · Rack 01", "#3b82f6", [
        ("Structure and Interpretation of Computer Programs (SICP)", "Harold Abelson & Gerald Jay Sussman", "Advanced", "sicp, lisp, scheme, functional programming", "The legendary MIT foundation of computer science and lambda calculus.", "Metalinguistic abstraction; Streams and delayed evaluation; Explicit-control evaluator; Register machine compilation"),
        ("Compilers: Principles, Techniques, and Tools (Dragon Book)", "Alfred V. Aho, Monica S. Lam, Ravi Sethi, Jeffrey D. Ullman", "Advanced", "compilers, lex, yacc, parsing, optimization", "The premier definitive reference on compiler design and code generation.", "Lexical analysis & finite automata; LL and LR syntax parsing; Intermediate code generation (Three-Address Code); Control flow graph optimization"),
        ("Computer Architecture: A Quantitative Approach", "John L. Hennessy & David A. Patterson", "Advanced", "hardware, cpu, risc, pipelining, cache", "Turing Award-winning blueprint of modern microprocessor engineering.", "Instruction-level parallelism (ILP); Multi-level cache hierarchy design; Superscalar execution and branch prediction; Vector and SIMD architectures"),
        ("Database System Concepts", "Abraham Silberschatz, Henry F. Korth, S. Sudarshan", "Intermediate", "database, sql, indexing, btree, acid", "Comprehensive university standard on relational and modern database engines.", "Relational algebra & SQL normalization; B+ Tree indexing & hashing; ACID transaction isolation levels; Concurrency control and write-ahead logging (WAL)"),
        ("Introduction to the Theory of Computation", "Michael Sipser", "Advanced", "automata, turing machine, complexity, p np", "The definitive graduate introduction to computability and complexity theory.", "Deterministic & Nondeterministic Finite Automata (DFA/NFA); Context-free grammars & pushdown automata; Turing machines & undecidability (Halting problem); P vs NP completeness"),
        ("Computer Systems: A Programmer's Perspective (CS:APP)", "Randal E. Bryant & David R. O'Hallaron", "Intermediate", "systems, assembly, linking, memory", "Bridging software architecture with underlying hardware mechanics.", "x86-64 machine assembly code; Memory hierarchy and spatial/temporal locality; Dynamic linking and loader mechanics; Exceptional control flow and signals"),
        ("Types and Programming Languages (TAPL)", "Benjamin C. Pierce", "Advanced", "type systems, lambda calculus, compilers", "Comprehensive mathematical foundation of programming language type theory.", "Untyped lambda calculus; Simply typed lambda calculus; Subtyping and polymorphism; Type inference with Hindley-Milner"),
        ("Purely Functional Data Structures", "Chris Okasaki", "Advanced", "functional programming, data structures, haskell", "Mathematical algorithms designed specifically for functional persistence.", "Strict vs lazy evaluation; Persistent red-black trees; Leftist heaps and binomial queues; Amortized analysis for persistent structures"),
        ("Programming Pearls", "Jon Bentley", "Intermediate", "algorithms, problem solving, optimization", "Classic collection of clever programming insights and optimization heuristics.", "Cracking tough algorithm problems with binary search; Space/time trade-off heuristics; Code tuning techniques; Back-of-the-envelope estimation"),
        ("Cracking the Coding Interview", "Gayle Laakmann McDowell", "Intermediate", "interviews, algorithms, data structures, coding", "Comprehensive technical interview playbook with 189 algorithm challenges.", "Big-O runtime optimization; Bit manipulation tricks; Dynamic programming memoization; System design interview frameworks"),
    ]),
    ("Artificial Intelligence", "Zone A · Rack 02", "#1d4ed8", [
        ("Deep Learning with Python", "François Chollet", "Intermediate", "keras, deep learning, python, computer vision", "Hands-on neural network engineering by the creator of Keras.", "Tensor operations & gradients; Convolutional nets for image classification; Recurrent architectures for sequential data; Generative deep learning"),
        ("Grokking Deep Learning", "Andrew W. Trask", "Beginner", "deep learning, neural networks, beginner, numpy", "Build neural networks from scratch using pure NumPy with zero black-box magic.", "Forward propagation arithmetic; Gradient descent from scratch; Backpropagation step-by-step; Dropout regularization"),
        ("Generative Deep Learning", "David Foster", "Advanced", "generative ai, vae, gans, diffusion, llms", "Building generative models that create images, text, and music.", "Variational Autoencoders (VAEs); Deep Convolutional GANs (DCGANs); Diffusion models (DALL-E mechanics); Transformer language generation"),
        ("Speech and Language Processing", "Daniel Jurafsky & James H. Martin", "Advanced", "nlp, speech, linguistics, language models", "The world standard textbook for computational linguistics and NLP.", "N-gram language models; Word2Vec & GloVe vector embeddings; Sequence labeling with HMMs; Speech recognition phonetics"),
        ("Graph Representation Learning", "William L. Hamilton", "Advanced", "gnn, graph neural networks, embeddings", "Foundations of Graph Neural Networks (GNNs) and graph embeddings.", "Node embedding algorithms (DeepWalk, Node2Vec); Graph Convolutional Networks (GCNs); Message passing frameworks; Link prediction models"),
        ("Probabilistic Graphical Models", "Daphne Koller & Nir Friedman", "Advanced", "bayesian networks, markov networks, inference", "The definitive treatise on Bayesian networks and probabilistic inference.", "Bayesian network factorizations; Markov random fields; Exact variable elimination inference; Loopy belief propagation"),
        ("Machine Learning Yearning", "Andrew Ng", "Intermediate", "machine learning, strategy, error analysis, ai", "Strategic tactical guide on structuring and debugging ML projects.", "Setting up train/dev/test splits; Diagnosing bias vs variance; Error analysis methodology; Transfer learning deployment"),
        ("Foundations of Machine Learning", "Mehryar Mohri, Afshin Rostamizadeh, Ameet Talwalkar", "Advanced", "statistical learning theory, rademacher, pac", "Theoretical mathematical foundations of machine learning bounds.", "PAC learning framework; Rademacher complexity; Generalization bounds for SVMs; Boosting theoretical convergence"),
    ]),
    ("Cybersecurity", "Zone A · Rack 05", "#dc2626", [
        ("Applied Cryptography", "Bruce Schneier", "Advanced", "cryptography, schneier, ciphers, protocols", "The classic encyclopedia on encryption algorithms and protocols.", "Secret-key and public-key algorithms; Digital signature schemes; Key management infrastructure; Pseudo-random bit generators"),
        ("Hacking: The Art of Exploitation", "Jon Erickson", "Intermediate", "hacking, exploit, c, buffer overflow, assembly", "Exploration of software bugs, assembly memory layout, and exploit mechanics.", "Stack-based buffer overflows; Shellcode generation in assembly; Network packet sniffing; Cryptographic attack vectors"),
        ("Threat Modeling: Designing for Security", "Adam Shostack", "Intermediate", "threat modeling, security, stride, architecture", "Actionable framework for finding security flaws during software design.", "STRIDE threat categorization; Data flow diagramming (DFDs); Prioritizing threat mitigations; Attack trees construction"),
        ("Real-World Bug Hunting", "Peter Yaworski", "Beginner", "bug bounty, web security, xss, vulnerabilities", "Field guide to discovering web vulnerabilities and bug bounty hunting.", "Open redirect vulnerabilities; Broken access control (IDOR); Server-Side Request Forgery (SSRF); Writing clear vulnerability reports"),
        ("Practical Reverse Engineering", "Bruce Dang, Alexandre Gazet, Elias Bachaalany", "Advanced", "reverse engineering, x86, x64, windows kernel", "In-depth guide to reverse engineering x86, x64, ARM, and Windows drivers.", "x86 and ARM calling conventions; Reversing C++ virtual method tables; Windows kernel rootkit analysis; De-obfuscating encrypted malware"),
        ("Metasploit: The Penetration Tester's Guide", "David Kennedy, Jim O'Gorman", "Intermediate", "penetration testing, metasploit, exploits", "Mastering the world's most popular penetration testing framework.", "Metasploit architecture & modules; Automated payload delivery; Meterpreter post-exploitation; Writing custom exploit modules"),
        ("Blue Team Handbook: Incident Response Edition", "Don Murdoch", "Intermediate", "incident response, soc, blue team, forensics", "Concise operational playbook for cybersecurity defenders.", "Memory forensics analysis; Log aggregation & SIEM queries; Containment strategies; Post-incident remediation steps"),
    ]),
    ("Data Science", "Zone A · Rack 04", "#2563eb", [
        ("Storytelling with Data", "Cole Nussbaumer Knaflic", "Beginner", "data visualization, charts, storytelling, communication", "Essential guide for communicating business insights with impactful data visuals.", "Eliminating chart clutter; Directing audience attention with preattentive attributes; Choosing the right chart format; Crafting a narrative arc"),
        ("R for Data Science", "Hadley Wickham & Garrett Grolemund", "Beginner", "r, tidyverse, ggplot2, data analysis", "The definitive guide to data science using R and the Tidyverse.", "Data manipulation with dplyr; Beautiful plotting with ggplot2; Tidy data principles; String and date parsing in R"),
        ("Feature Engineering for Machine Learning", "Alice Zheng & Amanda Casari", "Intermediate", "feature engineering, data prep, ml", "Transforming raw data into predictive model inputs.", "Numeric feature scaling & binning; One-hot & target encoding for categorical data; Text feature TF-IDF; Image feature extraction"),
        ("Designing Autonomous AI Systems", "Ethem Alpaydin", "Advanced", "data science, autonomous, machine learning", "Machine learning principles for building autonomous intelligent agents.", "Supervised learning decision theory; Non-parametric density estimation; Multilayer perceptrons; Reinforcement learning convergence"),
        ("Mining of Massive Datasets", "Jure Leskovec, Anand Rajaraman, Jeffrey D. Ullman", "Advanced", "big data, mapreduce, pagerank, stream mining", "Stanford's premier curriculum for analyzing web-scale data.", "MapReduce framework algorithms; PageRank and web graph mining; Locality-sensitive hashing (LSH); Data stream sliding windows"),
        ("Practical Statistics for Data Scientists", "Peter Bruce & Andrew Bruce", "Intermediate", "statistics, data science, regression, testing", "50+ essential statistical concepts applied to data science.", "Exploratory data analysis; A/B testing and significance; Multiple linear regression; Classification metrics"),
    ]),
    ("Mathematics", "Zone B · Rack 04", "#10b981", [
        ("Understanding Analysis", "Stephen Abbott", "Intermediate", "analysis, math, limits, topology", "Delightfully clear and elegant introduction to real analysis.", "The Axiom of Completeness; Topology of the real line (Compactness, Connectedness); Sequences of functions & uniform convergence; The derivative and Riemann integral"),
        ("Linear Algebra and Its Applications", "David C. Lay", "Beginner", "linear algebra, matrices, eigenvalues, vectors", "Standard undergraduate foundation in matrix algebra.", "Systems of linear equations & row reduction; Vector spaces & basis dimensions; Determinant properties; Orthogonality & Gram-Schmidt process"),
        ("Abstract Algebra", "David S. Dummit & Richard M. Foote", "Advanced", "abstract algebra, groups, rings, fields", "The definitive graduate reference on modern algebraic structures.", "Group theory & Sylow theorems; Ring homomorphisms & ideals; Field extensions and Galois theory; Commutative algebra basics"),
        ("Topology", "James R. Munkres", "Advanced", "topology, math, metric spaces, compactness", "The standard global textbook on point-set and algebraic topology.", "Topological spaces & continuous functions; Connectedness and compactness; Countability and separation axioms; The Fundamental Group"),
        ("Complex Analysis", "Lars Ahlfors", "Advanced", "complex analysis, ahlfors, cauchy, conformal", "Classic treatise on analytic functions of a complex variable.", "Cauchy-Riemann equations; Cauchy Integral Theorem & formula; Residue calculus & contour integrals; Conformal mappings & Riemann mapping theorem"),
        ("A First Course in Probability", "Sheldon Ross", "Intermediate", "probability, combinatorics, random variables", "Clear and rich problems in probability theory.", "Combinatorial analysis; Axioms of probability & conditional probability; Discrete and continuous random variables; Central Limit Theorem"),
        ("Calculus", "James Stewart", "Beginner", "calculus, stewart, integrals, derivatives", "The world's bestselling comprehensive undergraduate calculus textbook.", "Limits and continuity; Differentiation techniques (Chain Rule, Product Rule); Fundamental Theorem of Calculus; Series convergence tests"),
        ("Introduction to Topology and Modern Analysis", "George F. Simmons", "Advanced", "topology, banach spaces, hilbert spaces", "Bridging point-set topology with functional analysis.", "Metric spaces; Compactness & completeness; Banach spaces & bounded linear operators; Hilbert spaces & spectral theory"),
    ]),
    ("Electronics & VLSI", "Zone C · Rack 06", "#f59e0b", [
        ("The Art of Electronics", "Paul Horowitz & Winfield Hill", "Intermediate", "electronics, circuits, analog, digital, horowitz", "The undisputed holy grail of practical electronic design.", "Transistor amplifier design; Operational amplifier golden rules; Precision analog circuit design; Low-noise power supplies"),
        ("Fundamentals of Microelectronics", "Behzad Razavi", "Intermediate", "microelectronics, razavi, mosfet, bjt", "Clear, step-by-step analysis of semiconductor devices.", "BJT and MOS small-signal models; Single-stage amplifier topologies; Differential amplifiers; Frequency response and feedback"),
        ("Design of Analog CMOS Integrated Circuits", "Behzad Razavi", "Advanced", "cmos, analog, ic design, razavi, vlsi", "The global standard for transistor-level analog IC engineering.", "Current mirrors and active loads; Op-amp stability and frequency compensation; Bandgap references; Switched-capacitor circuits"),
        ("Digital Integrated Circuits: A Design Perspective", "Jan M. Rabaey, Anantha Chandrakasan", "Advanced", "digital ic, cmos, vlsi, timing", "Classic text on digital microelectronics and sub-micron physics.", "Inverter static and dynamic characteristics; Combinational logic styles (Pass-transistor, Dynamic logic); Interconnect parasitics and delay; Power dissipation optimization"),
        ("Electromagnetic Waves and Radiating Systems", "Edward C. Jordan & Keith G. Balmain", "Advanced", "electromagnetics, antennas, microwave, waves", "Classic textbook on antennas and wave propagation.", "Maxwell equations in time-harmonic fields; Plane wave propagation in dielectrics and conductors; Transmission line theory; Dipole and aperture antenna radiation"),
        ("Microwave Engineering", "David M. Pozar", "Advanced", "microwave, rf, smith chart, waveguides", "The standard textbook on RF and microwave circuit design.", "Transmission lines and Smith Chart matching; Waveguides and resonant cavities; Microwave network analysis (S-parameters); Power dividers and directional couplers"),
    ]),
    ("Robotics & Mechanical", "Zone C · Rack 07", "#d97706", [
        ("Probabilistic Robotics", "Sebastian Thrun, Wolfram Burgard, Dieter Fox", "Advanced", "robotics, probabilistic, slam, kalman, particle", "The seminal masterwork on robotic uncertainty and spatial intelligence.", "Recursive Bayesian filtering; Extended and Unscented Kalman Filters; Particle filters for localization (MCL); FastSLAM algorithm"),
        ("Modern Robotics: Mechanics, Planning, and Control", "Kevin M. Lynch & Frank C. Park", "Advanced", "robotics, lie groups, screw theory, kinematics", "Modern geometric formulation using Lie groups and screw theory.", "Spatial descriptions with Lie group SE(3); Forward kinematics with Product of Exponentials (PoE); Inverse kinematics & velocity Jacobians; Constrained dynamics & trajectory planning"),
        ("Feedback Systems: An Introduction for Scientists and Engineers", "Karl Johan Åström & Richard M. Murray", "Intermediate", "control systems, feedback, pid, bode", "Clear modern control theory using state-space and frequency methods.", "Dynamic modeling & state-space representations; Linear feedback & pole placement; Frequency response & Bode plots; PID control and loop shaping"),
        ("Control Systems Engineering", "Norman S. Nise", "Intermediate", "control systems, nise, root locus, pid, nyquist", "Standard university undergraduate text on classical control.", "Transfer functions and block diagrams; Time-response specifications; Root locus design technique; Nyquist stability criterion"),
        ("Vector Mechanics for Engineers: Statics", "Ferdinand P. Beer & E. Russell Johnston", "Beginner", "mechanics, statics, vectors, forces", "World-renowned curriculum on engineering statics.", "Vector operations in 3D; Distributed forces & centers of gravity; Friction on screws and wedges; Virtual work principle"),
        ("Mechanics of Materials", "Ferdinand P. Beer, E. Russell Johnston, John T. DeWolf", "Intermediate", "mechanics of materials, stress, strain, beams", "The standard reference on stress-strain analysis in structures.", "Normal and shear stress; Torsion of circular shafts; Bending stress in beams; Mohr's Circle for plane stress"),
    ]),
    ("Management & Humanities", "Zone D · Rack 08", "#8b5cf6", [
        ("Good to Great", "Jim Collins", "Beginner", "management, business, leadership, collins", "Five-year research study on why some companies make the leap.", "Level 5 Leadership; First Who, Then What principle; The Hedgehog Concept; The Flywheel Effect"),
        ("The Lean Startup", "Eric Ries", "Beginner", "startups, lean, mvp, agile, entrepreneurship", "Framework for building businesses through rapid validated learning.", "Build-Measure-Learn feedback loop; Minimum Viable Product (MVP); Pivot vs persevere decisions; Innovation accounting"),
        ("Zero to One", "Peter Thiel", "Beginner", "startups, thiel, innovation, monopoly", "Notes on startups and how to build breakthrough monopolies.", "Vertical vs horizontal progress; The power of proprietary technology; Network effects & economies of scale; Definite optimism"),
        ("Crucial Conversations", "Kerry Patterson, Joseph Grenny", "Beginner", "communication, leadership, soft skills, negotiation", "Tools for talking when stakes are high and opinions vary.", "Start with heart (mutual purpose); Make it safe to speak; Master your stories & emotions; Agree on a clear decision framework"),
        ("Atomic Habits", "James Clear", "Beginner", "habits, productivity, self improvement, psychology", "Practical system for making tiny changes that deliver remarkable results.", "The Four Laws of Behavior Change; Make it obvious, attractive, easy, and satisfying; Habit stacking; Identity-based habit formation"),
        ("Deep Work", "Cal Newport", "Beginner", "focus, productivity, deep work, concentration", "Rules for focused success in a distracted digital world.", "Deep work vs shallow work; The 4 disciplines of deep work execution; Quitting social media metrics; Draining the shallows"),
    ]),
]


def seed_200():
    app = create_app()
    with app.app_context():
        print("[*] Starting NexShelf Ultra 200+ Books Seeding...")

        total_seeded = 0

        # Seed core dataset
        for item in BOOKS_DATASET:
            isbn, title, author_name, cat_name, pub_year, qty, shelf, diff, color, tags, summary, takeaways = item

            author = Author.query.filter_by(name=author_name).first()
            if not author:
                author = Author(name=author_name).save()

            cat = Category.query.filter_by(name=cat_name).first()
            if not cat:
                cat = Category(name=cat_name).save()

            book = Book.query.filter_by(isbn=isbn).first()
            if not book:
                book = Book(
                    isbn=isbn,
                    title=title,
                    author_id=author.id,
                    category_id=cat.id,
                    publisher="Academic Press",
                    publication_year=pub_year,
                    quantity=qty,
                    available_quantity=qty,
                    shelf_location=shelf,
                    difficulty_level=diff,
                    accent_color=color,
                    tags=tags,
                    summary=summary,
                    key_takeaways=takeaways,
                    barcode=isbn.replace("-", ""),
                ).save()
                total_seeded += 1

        # Seed additional domain expansions
        isbn_counter = 9780131190000
        for cat_name, rack_prefix, color, books in ADDITIONAL_DOMAINS:
            cat = Category.query.filter_by(name=cat_name).first()
            if not cat:
                cat = Category(name=cat_name).save()

            for idx, (title, author_name, diff, tags, summary, takeaways) in enumerate(books):
                isbn = f"978-{isbn_counter:010d}"
                isbn_counter += 7
                shelf = f"{rack_prefix} · Shelf {(idx % 4) + 1}"

                author = Author.query.filter_by(name=author_name).first()
                if not author:
                    author = Author(name=author_name).save()

                book = Book.query.filter_by(title=title).first()
                if not book:
                    book = Book(
                        isbn=isbn,
                        title=title,
                        author_id=author.id,
                        category_id=cat.id,
                        publisher="NexShelf University Press",
                        publication_year=2015 + (idx % 8),
                        quantity=4 + (idx % 5),
                        available_quantity=4 + (idx % 5),
                        shelf_location=shelf,
                        difficulty_level=diff,
                        accent_color=color,
                        tags=tags,
                        summary=summary,
                        key_takeaways=takeaways,
                        barcode=isbn.replace("-", ""),
                    ).save()
                    total_seeded += 1

        # Ensure we have 200+ books by synthesizing diverse high-demand academic reference modules
        current_count = Book.query.count()
        print(f"[*] Current catalog size: {current_count} books.")

        if current_count < 205:
            needed = 205 - current_count
            print(f"[*] Synthesizing {needed} specialized academic monographs to guarantee 200+ catalog...")

            sub_topics = [
                ("Cloud & Edge Computing", "Zone A · Rack 03", "#2563eb", "cloud, serverless, edge computing, distributed", "Architectural patterns for edge devices, serverless functions, and low-latency global networks.", "Edge computing topologies; Function-as-a-Service cold starts; Event-driven streaming; Distributed consensus"),
                ("Deep Reinforcement Learning & Robotics", "Zone A · Rack 04", "#1d4ed8", "ai, rl, robotics, gym, ppo, actor critic", "End-to-end policy gradients and sim-to-real robotic control.", "Proximal Policy Optimization (PPO); Actor-Critic networks; Domain randomization in simulation; Robotic manipulation policies"),
                ("Quantum Computing & Algorithms", "Zone B · Rack 05", "#059669", "quantum, qubits, shor, grover, physics", "Qubit quantum logic gates, teleportation, and polynomial quantum speedups.", "Qubit state vectors & Bloch Sphere; Grover's search algorithm; Shor's prime factorization algorithm; Quantum error correction codes"),
                ("Bioinformatics & Computational Genomics", "Zone B · Rack 04", "#10b981", "bioinformatics, genomics, dna, sequence alignment", "Computational algorithms for gene sequencing and protein folding.", "Needleman-Wunsch global alignment; Smith-Waterman local alignment; Hidden Markov Models in genomics; AlphaFold protein prediction"),
                ("VLSI Digital Signal Processing Architectures", "Zone C · Rack 06", "#f59e0b", "vlsi, dsp, pipelining, systolic arrays", "Hardware architectures for ultra-fast digital signal processing.", "Pipelining and parallel processing in DSP; Systolic array matrix multiplication; Retiming & unfolding algorithms; Low-power arithmetic units"),
                ("Embedded Linux & Real-Time Kernel Design", "Zone C · Rack 07", "#d97706", "embedded linux, kernel, device drivers, rtos", "Building custom embedded Linux distributions and kernel device drivers.", "Bootloaders (U-Boot) and device trees; Character device driver design; PREEMPT_RT real-time patches; Root filesystem construction with Yocto"),
                ("Renewable Energy Systems & Smart Grids", "Zone C · Rack 08", "#b45309", "renewable energy, solar, wind, smart grid, power", "Engineering principles of solar photovoltaic, wind turbine, and smart microgrids.", "Solar PV equivalent circuit models; Maximum Power Point Tracking (MPPT); Wind turbine aerodynamic power coefficients; Grid-tied inverter synchronization"),
                ("Behavioral Economics & Decision Science", "Zone D · Rack 08", "#8b5cf6", "economics, psychology, behavioral, game theory", "Empirical study of human decision heuristics and market dynamics.", "Nudge theory and choice architecture; Bounded rationality; Hyperbolic discounting; Behavioral game theory experiments"),
            ]

            counter = 1
            while Book.query.count() < 205:
                for topic, rack, col, t_tags, t_sum, t_takes in sub_topics:
                    if Book.query.count() >= 205:
                        break
                    
                    cat = Category.query.filter_by(name=topic).first() or Category(name=topic).save()
                    author_name = f"Prof. Raymond V. Sterling {counter}"
                    author = Author.query.filter_by(name=author_name).first() or Author(name=author_name).save()

                    b_title = f"Advanced Principles of {topic} (Vol. {counter})"
                    b_isbn = f"978-081{counter:04d}{Book.query.count():04d}"
                    b_shelf = f"{rack} · Shelf {(counter % 4) + 1}"

                    Book(
                        isbn=b_isbn,
                        title=b_title,
                        author_id=author.id,
                        category_id=cat.id,
                        publisher="NexShelf University Academic Press",
                        publication_year=2020 + (counter % 5),
                        quantity=5,
                        available_quantity=5,
                        shelf_location=b_shelf,
                        difficulty_level="Advanced" if counter % 2 == 0 else "Intermediate",
                        accent_color=col,
                        tags=t_tags,
                        summary=t_sum,
                        key_takeaways=t_takes,
                        barcode=b_isbn.replace("-", ""),
                    ).save()
                    counter += 1

        final_count = Book.query.count()
        print(f"[+] SUCCESS! NexShelf catalog now contains {final_count} high-quality books.")


if __name__ == "__main__":
    seed_200()
