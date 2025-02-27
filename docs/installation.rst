Installation
============

Basic Installation
-----------------

You can install the Adaptive Cards Toolkit using pip:

.. code-block:: bash

    pip install adaptive-cards-toolkit

This will install the basic toolkit with the required dependencies.

Dependencies
-----------

The Adaptive Cards Toolkit requires Python 3.7 or later and has the following dependencies:

- adaptive-cards-py >= 0.2.4
- requests >= 2.25.0

Optional Dependencies
--------------------

For OpenAI integration (to generate cards using natural language), you can install the optional dependencies:

.. code-block:: bash

    pip install adaptive-cards-toolkit[openai]

Or manually:

.. code-block:: bash

    pip install openai>=1.0.0

Development Installation
-----------------------

If you want to contribute to the development of Adaptive Cards Toolkit, you can install the development dependencies:

.. code-block:: bash

    git clone https://github.com/yourusername/adaptive-cards-toolkit.git
    cd adaptive-cards-toolkit
    pip install -e ".[dev]"

This will install the package in development mode along with all the development dependencies like testing, linting, and documentation tools.