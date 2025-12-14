import pyttsx3
engine = pyttsx3.init()

# speaking engine
def speak(text):

    engine.say(text)
    engine.runAndWait()

# escape function
def escape():
    print("You ordered nothing")
    speak("You ordered nothing")
    exit()

# our Menu
menu = {
    "popcorn" :   90,
    "colddrink" : 70,
    "biryani" :   250,
    "tikka" :     400, 
    "mintdrink":  80,
    "coffee":     100
}

# specifying the quantity for items in menu per item
quantity_check_list = ["Medium Pack" , "1 litre" , "1 kg" , "1 kg" , "500ml", "250ml"]
copied_menu = menu.copy() # Copying the original menu to display the order at the end

cart = {} # An empty dictionary for storing order
total = 0


print("\tThe Bey's Mutfak ")
print("------------ Menu --------------")

# Displaying the menu
i = 1 # for displpaying menu's index
j = 0
for key, value in menu.items():
    print(f"{i}- {key.capitalize():20} : Rs{value:10}/- \t {quantity_check_list[j]}")
    i +=1
    j +=1

menu_list = list(menu.keys())

demand = True
speak("What would you like to order!")

while demand:

    order = input("What would you like to order(Enter \' B \' for bill and \' Q \' to quit): ").lower() # Taking order from user

    order = order.replace(" ", "") # Handeling Spaces

    # exits the program if q or b is entered
    if order in ("q", 'b'): 
        demand = False
        if not cart:
            escape()
        continue

    # Check if the input is a digit (numeric order)
    if order.isdigit():
        order_int = int(order)
        if 1 <= order_int <= len(menu_list):  # Ensure the number is within the menu range
            order = menu_list[order_int - 1]  # Map the number to the menu item
        else:
            print("Invalid order")
            continue

    # Check if the input is a valid menu item (string order)
    elif order not in menu:
        print("Invalid order")
        continue

    # asking for quantity
    while True:
        try:
            # specifying format according to the order
            if order == "colddrink":
                quantity = int(input(f"Enter the quantity for {order} per 1 liter: "))
            elif order == "popcorn":
                quantity = int (input(f"Enter the quantity for {order} 1 medium pack: "))
            elif order == "biryani":
                quantity = int (input(f"Enter the quantity for {order}, 1kg: "))
            elif order == "tikka":
                quantity = int (input(f"Enter the quantity for {order}, 1 kg: "))
            elif order == "mintdrink":
                quantity = int (input(f"Enter the quantity for {order}, 500ml: "))
            elif order == "coffee":
                quantity = int(input(f"Enter the quantity for {order}, 250ml: "))

            quantity = int(quantity) # type: ignore

            if quantity<=0:
                print("Enter the valid quantity")
                continue
            else:
                break
        except ValueError:
            print("Enter the valid quantity")
            continue
        #inner while loop ends

    # adding order to cart (outer while loop continued)
    if order in menu:
        if order in cart:
            cart[order] += quantity
        else:
            cart[order] = quantity
            total += menu[order] * quantity  
        
# Displaying the order
print("\t------------ Your Order --------------\n")
i =1 
for item, quantity in cart.items():
    print(f"{i}. {item.capitalize()} : Rs.{menu[item] * quantity}/- 1. = Rs.{copied_menu[item]}, Total Quantity : {quantity}\n")
    i+=1

total_items = len(cart)
print(f'Total items are : {total_items}')

speak(f"Total Bill : Rupees {total}")
print(f"\nTotal Bill : Rs {total}/-")

# returning module.....

loop_for_return = True
while loop_for_return:  # infinite loop for checking wheather the user want to return anything more
    try:
        return_decision = input("Wanna return something...(Y/N): ").lower()
        
        if return_decision not in ('y', 'n'):
            print("Invalid input")
            continue

        if return_decision =='y':
            return_item = input("Enter the item name or number you want to return: ")
            
            # checking if the user enters the number for returning the item
            if return_item.isdigit() or (return_item.startswith('-') and return_item[1:].isdigit()):
                return_item_int = int(return_item)  # Convert to integer
                if return_item_int <= 0:
                    print("Enter valid input")
                    continue

                cart_list = list(cart)  # Convert cart dict to list
                if 1 <= return_item_int <= len(cart_list):  # Ensure the number is valid
                    return_item = cart_list[return_item_int - 1]  # Fetch the return item

                else:
                    print("Invalid item number. Please try again.")
                    continue
                    

            if return_item not in cart:
                print(f"{return_item} is not in your cart")
                continue
            # checking the return quantity 
            return_quantity = int(input(f"How many {return_item}s you want to return ? :  "))
            if return_quantity == 0 : # if return quantity is 0
                print("You returned nothing")    
                loop_for_return = False
                break

            elif return_quantity > cart[return_item]: # if user enter the quantity more than in his cart
                print("Enetred value is more than item in your cart")
                continue

            elif return_quantity < cart[return_item]: # if user enters the quantity less than item in cart ( valid data )
                remaining_item = cart[return_item] - return_quantity   
                cart[return_item] = remaining_item

            elif return_quantity == cart[return_item]: # if the return quantity is equals to quantity in cart
                del cart[return_item]

            print("------------ Your Order ---------------")
            i = 1 
            for item, quantity in cart.items():
                print(f"{i}. {item.capitalize()} : Rs.{menu[item] * quantity}/- 1. = Rs.{copied_menu[item]}, Total Quantity : {quantity}\n")
                i+=1
            naya_total = 0 
            for menu_item, new_total in cart.items():
                naya_total += new_total * menu[menu_item]

            total = naya_total
            print(f"Your Total bill now is {total}")

        elif return_decision == 'n':
            loop_for_return = False
            break
    except ValueError:
        print("Invalid input.")
        continue

# check out section 
print("------------ Check Out ---------------")
check_out_loop = True
while check_out_loop:

    if not cart:
        exit()

    try:
        deposit = input("Kindly  the billing amount: ")
        # checking if the deposit is valid or not
        if deposit.isdigit() == False:
            print("Enter the valid amount")
            continue
        
        # converting the deposit to integer
        else:
            deposit = int(deposit)

            if deposit<=0:
                print("Enter the valid amount")
                continue

            elif deposit < total:
                remaining_amount = total - deposit
                depositing_loop = True
                while depositing_loop:
                    try:
                        additional_deposit = int(input(f"You still need to pay Rs{remaining_amount}. Kindly deposit: "))
                    except ValueError:
                        print("Kindly Enter a valid value.")
                        continue

                    if additional_deposit < remaining_amount:
                        remaining_amount = remaining_amount - additional_deposit
                        # Handeling out the omissions during the deposit.
                        while True:
                            try:
                                re_deposit = int(input(f"You have given Rs{remaining_amount} less, kindly pay the amount: "))
                                
                                # if re_deposit.isdigit() == False:
                                #     print("Enter the valid amount")
                                #     continue

                                # handeling out the re deposit errors
                                if re_deposit <= 0:
                                    print("Enter a valid amount greater than 0")
                                    continue
                                
                                if re_deposit == remaining_amount:
                                    print("Thank you for your order")
                                    break
                                elif re_deposit > remaining_amount:
                                    change = re_deposit - remaining_amount
                                    print(f"Thank you for your order. Your change is Rs{change}/-")
                                    
                                    break
                                else:
                                    print(f"You still need to pay Rs{remaining_amount - re_deposit}.")
                                    remaining_amount -= re_deposit
                                    continue

                            except ValueError:
                                print("Enter a valid numeric amount")
                                continue
                        # breaking out of the inner and outer loops 
                        depositing_loop = False    
                        check_out_loop = False
                        break

                    elif additional_deposit > remaining_amount:
                        change = additional_deposit - remaining_amount
                        print(f"Thank you for your order. Your change is Rs{ change}/-")
                        check_out_loop = False
                        break

                    else:
                        print("Thank you for your order")
                        check_out_loop = False
                        break
                
                
            elif deposit > total:

                change = deposit - total
                speak(f"Thank you for your order.")
                print(f"Thank you for your order. Your change is Rs {change}/-")

                break

            elif deposit == total:
                speak(f"Thank you for your order.")
                print("Thank you for your order")
                break

    except ValueError:
        print("Enter the valid amount plz")
        continue

# user
while True:
    if not cart:
        exit()
        
    suggestion_choice = input("Do you have any suggestion for us? (Y/N): ").lower()
    if suggestion_choice == 'y':
        suggestion = input("Please write your suggesttion, We will be glad to hear: ")
        with open("user_suggestion.txt", "a") as sug_file:
            sug_file.write(suggestion + "\n\n")
        
        print("Thank you for visting \" Bey's Mutfak \" ")

        print("Recent suggestions")
        with open("user_suggestion.txt","r") as print_suggest:
            var= print_suggest.readlines()
            for suggestion in var:
                print(suggestion)

    elif suggestion_choice == 'n':
        print("Thank you for visting \" Bey's Mutfak \" ")
        speak("Eyvallah ! ")
        break

    else:
        print("Invalid choice")
        continue

