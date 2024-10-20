import tkinter as tk
from tkinter import font, scrolledtext

from setOperationsHandler import SetOperationsHandler
from textAsADict.textToDictionary import TextToDictionary


class VerbApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Verb Infinitive App")

        self.root.geometry("800x600")

        self.main_color = "#eed9c4"
        self.active_color = "#a9957b"
        self.root.configure(bg=self.main_color)

        large_font = font.Font(root=self.root, family="Courier", size=24, weight="bold")
        smaller_font = font.Font(root=self.root, family="Courier", size=12)

        self.text_dictionary  = TextToDictionary()
        self.verb_dict = self.text_dictionary.get_dictionary()

        self.set_operatorHandler = SetOperationsHandler()

        # Create and place the "App" label
        self.app_label = tk.Label(self.root, text="The Verb Assosiation Discovery App", font=large_font, bg=self.main_color)
        self.app_label.pack(pady=30)

        # Create and place the first instruction label
        instruction_label = tk.Label(self.root, text="Write an infinitive of a verb:", font=smaller_font,
                                     bg=self.main_color)
        instruction_label.pack()

        # Create and place the first text entry for user input
        self.verb_entry1 = tk.Entry(self.root, width=30, font=smaller_font)
        self.verb_entry1.pack(pady=20)

        # Create the button frame and place it below the first input
        button_frame = tk.Frame(self.root, bg=self.main_color)
        button_frame.pack(pady=20)

        # Create the buttons inside the button frame
        sum_button = tk.Button(button_frame, text="Sum", font=smaller_font, bg=self.main_color,
                               command=lambda : self.submit_operation("Sum", sum_button))
        sum_button.pack(side=tk.LEFT, padx=5)
        intersection_button = tk.Button(button_frame, text="Intersection", font=smaller_font, bg=self.main_color,
                                        command=lambda :self.submit_operation("Intersection", intersection_button))
        intersection_button.pack(side=tk.LEFT, padx=5)
        difference_button = tk.Button(button_frame, text="Difference", font=smaller_font, bg=self.main_color,
                                      command=lambda:self.submit_operation("Difference", difference_button))
        difference_button.pack(side=tk.LEFT, padx=5)

        self.operation_buttons = {}
        self.operation_buttons["Sum"] = sum_button
        self.operation_buttons["Intersection"] = intersection_button
        self.operation_buttons["Difference"] = difference_button


        # Create and place the second instruction label
        instruction_label2 = tk.Label(self.root, text="Write infinitives of verbs, comma separated:", font=smaller_font,
                                      bg=self.main_color)
        instruction_label2.pack()

        # Create and place the second text entry for user input
        self.verb_entry2 = tk.Entry(self.root, width=30, font=smaller_font)
        self.verb_entry2.pack(pady=10)

        # Add a button to submit the verb
        submit_button = tk.Button(self.root, text="Submit", command=self.submit_verb, font=smaller_font,
                                  bg=self.main_color)
        submit_button.pack(pady=20)

        self.result_descr_label = tk.Label(self.root, text="The result of your operation:", font=smaller_font,
                                           bg=self.main_color)
        self.result_descr_label.pack()

        # Create a scrolled text widget to display the result
        self.result_text = scrolledtext.ScrolledText(self.root, font=smaller_font, bg=self.main_color, wrap=tk.WORD,
                                                     height=10, width=80)
        self.result_text.pack(pady=10)

        # Initialize selected operation as None
        self.selected_operation = None

    def submit_verb(self):
        # Get the verb from the entry fields
        verb1 = self.verb_entry1.get().strip()
        verbs2 = set([v.strip() for v in self.verb_entry2.get().split(",") if v.strip()])

        # Check if an operation is selected, and if inputs are provided
        if not self.selected_operation:
            self.show_result("Please select an operation.")
        elif not verb1:
            self.show_result("Please enter the first verb.")
        elif not verbs2:
            self.show_result("Please enter at least one verb in the second input.")
        else:
            # Perform the operation
            result = self.set_operatorHandler.perform_set_operations(verb1, verbs2, self.selected_operation, self.verb_dict)
            # Show the result in the result text widget
            self.show_result(result)

    def submit_operation(self, operation, button):
        # Set the selected operation
        self.selected_operation = operation
        # Update button colors to indicate the active operation
        for op_button in self.operation_buttons.values():
            op_button.config(bg=self.main_color)
        button.config(bg=self.active_color)
        # Automatically update the result based on the new selected operation
        self.submit_verb()

    def show_result(self, result):
        # Clear previous results and insert the new result
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result)


# Create the main window
root = tk.Tk()

# Create the app
app = VerbApp(root)

# Run the app
root.mainloop()
