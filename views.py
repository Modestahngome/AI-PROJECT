from django.shortcuts import render
import random

# Create your views here.
def home(request):
    """
    Renders the home page of the dice guessing game.

    This is a simple view that serves as the entry point of the application,
    displaying the form where the user can input their number guess.

    Parameters:
        request (HttpRequest): The incoming HTTP request object provided
                               by Django's URL dispatcher.

    Returns:
        HttpResponse: Renders and returns the 'home.html' template with
                      no additional context — the page only needs the form.

    Notes:
        - This view only handles GET requests. POST logic is handled
          separately in the play() view to keep responsibilities clean.
    """
    return render(request, 'home.html')


def play(request):
    """
    Handles the core game logic for the dice guessing game.

    Accepts a POST request containing the user's number guess, validates
    the input, generates a random number to simulate a dice roll, compares
    the two, and returns a win/loss result to the user.

    Only processes POST requests — any other method (e.g. a direct GET
    to this URL) safely falls through to re-render the home page.

    Parameters:
        request (HttpRequest): The incoming HTTP request object. Expected
                               to carry a POST payload with:
                               - 'number' (str): The user's guessed number,
                                 must be a digit between 1 and 6 inclusive.

    Returns:
        HttpResponse: One of the following depending on the outcome:
            - Renders 'result.html' with context:
                - 'user_number' (int): The number the user submitted.
                - 'system_number' (int): The randomly generated dice number.
                - 'result' (str): Win or loss message shown to the user.
            - Renders 'home.html' with context:
                - 'error' (str): Validation message if input is missing
                  or out of the valid range.
            - Renders 'home.html' with no context if the request
              method is not POST.

    """
    if request.method == "POST":

        # Retrieve the raw string value submitted from the form.
        # .get() is used instead of direct key access to avoid a
        # KeyError if the 'number' field is missing from the request.
        user_number = request.POST.get('number')

        # Guard against empty submission — the form field may have been
        # submitted blank, which .get() would return as None or ''.
        if not user_number:
            return render(request, 'home.html', {
                'error': 'Please enter a number between 1 and 6'
            })

        # Convert from string to integer now that we know a value exists.
        # This must happen before the range check below.
        user_number = int(user_number)

        # Enforce the valid dice range. Values outside 1–6 are meaningless
        # in this game context and should be rejected with feedback.
        if user_number < 1 or user_number > 6:
            return render(request, 'home.html', {
                'error': 'Number must be between 1 and 6'
            })

        # Simulate a dice roll — randint is inclusive on both ends,
        # so this produces a fair value from 1 to 6.
        system_number = random.randint(1, 6)

        # Determine the outcome by comparing the user's guess to the
        # system's roll. An exact match is required to win.
        if user_number == system_number:
            result = "You Win! 🎉"
        else:
            result = "You Lose 😢"

        # Pass all relevant data to the result template so it can
        # display both numbers and the outcome to the user.
        return render(request, 'result.html', {
            'user_number': user_number,
            'system_number': system_number,
            'result': result
        })

    # If the request is not POST (e.g. user navigates directly to /play/),
    # redirect them back to the home page without any error or processing.
    return render(request, 'home.html')