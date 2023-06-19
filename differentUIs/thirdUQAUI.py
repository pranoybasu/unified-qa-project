import queries
import sys
from PyInquirer import prompt, style_from_dict, Token

# Define custom styles for PyInquirer
custom_style = style_from_dict({
    Token.QuestionMark: '#E91E63 bold',
    Token.Selected: '#673AB7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#2196f3 bold',
    Token.Question: '',
})

# Define the questions for PyInquirer
questions = [
    {
        'type': 'list',
        'name': 'option',
        'message': 'Unified QA 1.0',
        'choices': [
            {'name': 'Get batches', 'value': '1'},
            {'name': 'Get rejects', 'value': '2'},
            {'name': 'Get medium matches', 'value': '3'},
            {'name': 'Get unmapped schools', 'value': '4'},
            {'name': 'Exit', 'value': '5'},
        ],
    }
]


def get_batches():
    batch_id = input("Enter the batch ID: ")
    batches = queries.get_batches(batch_id)
    if batches:
        print("Batch ID | Batch Name | Load Status | Record Stage | Admin Count | Score Count")
        for batch in batches:
            print(f"{batch[0]} | {batch[1]} | {batch[2]} | {batch[3]} | {batch[4]} | {batch[5]}")
    else:
        print("No batches found.")


def get_rejects():
    process_id = input("Enter the process ID: ")
    rejects = queries.get_rejects(process_id)
    if rejects:
        print("Process ID | Process Name | Reject Message | Reject Count")
        for reject in rejects:
            print(f"{reject[0]} | {reject[1]} | {reject[2]} | {reject[3]}")
    else:
        print("No rejects found.")


def get_medium_matches():
    batch_id = input("Enter the batch ID: ")
    matches = queries.get_medium_matches(batch_id)
    if matches:
        print("First Name | Middle Name | Last Name | Grade | Birthdate | Source School Code | Source Student ID | Mapped Student ID | Mapped State Student ID | Batch Name | Student Identity UUID")
        for match in matches:
            print(f"{match[0]} | {match[1]} | {match[2]} | {match[3]} | {match[4]} | {match[5]} | {match[6]} | {match[7]} | {match[8]} | {match[9]} | {match[10]}")
    else:
        print("No medium matches found.")


def get_unmapped_schools():
    batch_id = input("Enter the batch ID: ")
    schools = queries.get_unmapped_schools(batch_id)
    if schools:
        print("School Identity UUID | State Code | Local School Code | School Name")
        for school in schools:
            print(f"{school[0]} | {school[1]} | {school[2]} | {school[3]}")
    else:
        print("No unmapped schools found.")


def exit_program():
    print("Goodbye!")
    sys.exit()


# Map options to corresponding actions
actions = {
    '1': get_batches,
    '2': get_rejects,
    '3': get_medium_matches,
    '4': get_unmapped_schools,
    '5': exit_program,
}


def main():
    while True:
        answer = prompt(questions, style=custom_style)
        option = answer['option']
        action = actions.get(option)
        if action:
            action()
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
