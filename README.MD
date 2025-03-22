# The Flying Dutchman Bar Ordering System

This system is the final project by the group "Lost Ship (Python)" for Uppsala University's User Interface Programming I (1MD002) course. Its functionalities include bar ordering and back-end management.

## Members and Contribution

- **An-lung Hsiao**: Menu Processing, Undo and Redo, MVC integration and optimization
- **Jakob Pettersson**: Stock Management, Employee Interface, Order Processing
- **Kyra Kendall**: Responsive Design, Reservation system, Interface optimization
- **Ping-Han Chou**: Menu and Shopping Cart Processing, Drag and Drop, Payment Page
- **Shuai Guo** Multilingual Processing, VIP Interface pages, Login and Logout Processing

## Dependencies Pacakages

This project uses the following packages:

- **tkinter**
- **Pillow (PIL)** (for image processing)
- **os**
- **json**
- **copy**

## Chatbots
We used some AI to help refine and optimize our code, making it more concise and high-performing, and we learned valuable lessons throughout the process.

## Run the System

Execute `main.py`:

```sh
python main.py
```

## Time Reporting For Group And Members
We believe that everyone spent a significant amount of time on this project. We did not specifically track each person’s hours, and each individual made their own unique contributions. As a result, our collaboration was very enjoyable.

## Github Link
[bar-point-of-sale-system](https://github.com/neilchouGTX/bar-point-of-sale-system/)

## Directory Structure
```
The Flying Dutchman Bar Ordering System
├── DBFilesJSON
│   ├── dutchman_legacy_order.json
│   ├── dutchman_menu.json
│   ├── dutchman_order.json
│   ├── dutchman_reservation.json
│   ├── dutchman_table_beers_bought.json
│   ├── dutchman_table_beers_sold.json
│   ├── dutchman_table_cart.json
│   ├── dutchman_table_payments.json
│   ├── dutchman_table_sbl_beer_stock.json
│   ├── dutchman_table_users.json
│   ├── dutchman_VIP_account.json
│   └── dutchman_VIP_menu.json
├── images
├── learnTk
├── models
│   ├── BeerModelAndData.py
│   ├── CartModelAndData.py
│   ├── MenuModelAndData.py
│   ├── ReservationModelAndData.py
│   └── StockModelAndData.py
├── styles
│   └── style_config.py
├── views
│   ├── Cart_view.py
│   ├── Home_VIP_view.py
│   ├── Login_view.py
│   ├── Login_view(Old) version.py
│   ├── My_orders_view.py
│   ├── Order_view.py
│   ├── Order_view_new.py
│   ├── Payment_view.py
│   ├── Reservation_view.py
│   ├── Staff_view.py
│   └── Upper_view.py
├── Base_view.py
├── Controller_translations.py
├── Controller.py
├── main.py
├── Model.py
└── README.md
```