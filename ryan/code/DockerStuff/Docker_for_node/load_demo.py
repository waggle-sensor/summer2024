print(f"Congratulations on getting Docker to work!\n")

print(f"here are all of the models you can run. Please select a number:\n1:   Ollama LLava\n2:   Florence-2-Large\n3:   Florence-2-Base")

demo = input("What model would you like to run?: ")

def pickDemo(demo):
    match(demo):
        case "1":
             print("Ollama")
        case "2":
            print("Florcence Large")
        case "3":
            print("Florence Base")
        case "4":
            print("secret")
        case _:
            pickDemo(demo)
    return 5

pickDemo(demo)
            


