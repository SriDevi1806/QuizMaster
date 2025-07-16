import os
import json

class Question:
    """Represents a single MCQ with text, options, and correct answer"""
    def __init__(self, text, options, correct_index):
        """
        Initialize a question.
        
        :param text: Question text
        :param options: List of answer choices
        :param correct_index: Index of correct option (0-based)
        """
        self.text = text
        self.options = options
        self.correct_index = correct_index
    
    def is_correct(self, answer_index):
        """Check if selected answer is correct"""
        return answer_index == self.correct_index

class Quiz:
    """Manages a quiz session for a specific category"""
    def __init__(self, category):
        self.category = category
        self.questions = []
        self.score = 0
    
    def load_questions(self, file_path):
        """Load questions from JSON file"""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                for q in data['questions']:
                    self.questions.append(
                        Question(q['text'], q['options'], q['correct_index'])
                    )
            return True
        except Exception as e:
            print(f"Error loading questions: {e}")
            return False

    def start_quiz(self):
        """Run the quiz interaction"""
        self.score = 0  # Reset score
        print(f"\n{'='*50}")
        print(f"Starting {self.category} Quiz!".center(50))
        print(f"{'='*50}\n")
        
        for i, question in enumerate(self.questions, 1):
            print(f"Question {i}: {question.text}")
            for idx, option in enumerate(question.options):
                print(f"  {idx+1}. {option}")
            
            # Get valid user input
            while True:
                try:
                    choice = int(input("\nYour answer (1-4): "))
                    if 1 <= choice <= 4:
                        break
                    print("Invalid choice! Enter 1-4")
                except ValueError:
                    print("Please enter a number")
            
            # Check answer and update score
            if question.is_correct(choice-1):
                print("✓ Correct!")
                self.score += 1
            else:
                correct = question.options[question.correct_index]
                print(f"✗ Wrong! Correct answer: {correct}")
            print("-"*50)
        
        return self.score
    
    def show_result(self):
        """Display final results with feedback"""
        total = len(self.questions)
        percentage = (self.score / total) * 100
        
        print("\n" + "="*50)
        print("QUIZ RESULTS".center(50))
        print("="*50)
        print(f"Category:    {self.category}")
        print(f"Score:       {self.score}/{total}")
        print(f"Percentage:  {percentage:.1f}%")
        
        # Feedback based on performance
        if percentage >= 90:
            print("Feedback:    Excellent! 🎉")
        elif percentage >= 70:
            print("Feedback:    Good job! 👍")
        elif percentage >= 50:
            print("Feedback:    Fair effort! 🙂")
        else:
            print("Feedback:    Try again! 💪")
        print("="*50 + "\n")

class QuizManager:
    """Handles quiz selection and execution"""
    def __init__(self, quiz_dir="quizzes"):
        self.quiz_dir = quiz_dir
        self.quizzes = {}  # {category: Quiz instance}
        self.load_all_quizzes()
    
    def load_all_quizzes(self):
        """Load all available quizzes from directory"""
        if not os.path.exists(self.quiz_dir):
            os.makedirs(self.quiz_dir)
            print(f"Created {self.quiz_dir} directory. Add quiz JSON files.")
        
        for filename in os.listdir(self.quiz_dir):
            if filename.endswith('.json'):
                category = filename[:-5]  # Remove .json extension
                quiz = Quiz(category)
                file_path = os.path.join(self.quiz_dir, filename)
                if quiz.load_questions(file_path):
                    self.quizzes[category] = quiz
    
    def select_category(self):
        """Show category selection menu"""
        if not self.quizzes:
            print("No quizzes found! Add JSON files to /quizzes folder")
            return None
        
        print("\nAvailable Quiz Categories:")
        for i, category in enumerate(self.quizzes.keys(), 1):
            print(f"  {i}. {category}")
        
        while True:
            try:
                choice = input("\nSelect category (number) or 0 to exit: ")
                if choice == '0':
                    return None
                choice = int(choice)
                if 1 <= choice <= len(self.quizzes):
                    category = list(self.quizzes.keys())[choice-1]
                    return self.quizzes[category]
                print(f"Invalid choice! Enter 1-{len(self.quizzes)} or 0 to exit")
            except ValueError:
                print("Please enter a number")

    def start(self):
        """Main application loop"""
        print("\n" + "="*50)
        print("QUIZMASTER TERMINAL GAME".center(50))
        print("="*50)
        
        while True:
            quiz = self.select_category()
            if not quiz:
                break
            quiz.start_quiz()
            quiz.show_result()
            
            another = input("Take another quiz? (y/n): ").lower()
            if another != 'y':
                break
        
        print("\nThanks for playing! Goodbye 👋")

# Run the application
if __name__ == "__main__":
    manager = QuizManager()
    manager.start()