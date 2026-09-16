#### Web operation tutorial

#### 1. Homepage

- Visit https://production.56yhz.com/ in your browser

![image-01](/media/img/WechatIMG280.jpeg){ loading=lazy style="max-width: 100%" }

- The lower right is the sub-modules of GreaterWMS, and the buttons above are the APP download link of GreaterWMS, the github source code warehouse url of GreaterWMS, language selection, registration and login
- APP download link: download link for GWMS.apks
- Language: Describes the languages supported by GreaterWMS, currently supports Simplified/Traditional Chinese, French, Portuguese, Spanish, Russian, Arabic, Italian and Japanese.
- Register: Open the administrator's registration page
- Login: Enter the login page of the administrator/ordinary user

#### 2. Registration

- Click the Register button on the home page

![image-02](/media/img/register-en.jpeg){ loading=lazy style="max-width: 100%" }
-
- The registration here is limited to administrator registration, ordinary users are added by administrators or accounts with administrator privileges
- Enter the user name, password and confirmation password, please keep the password and confirmation password consistent to complete the registration
- The maximum character length supported here is 255 characters
- Automatic login after registration

#### 3. User login

- Click the login button on the homepage

![image-03](/media/img/userlogin-en.jpeg){ loading=lazy style="max-width: 100%" }

- If you logged in as a user last time, click Login this time to jump to the user login page
- Your OPENID: unique, provided by the administrator
- Username and Verification Code: Provided by the administrator, if the input is consistent, the login is successful, otherwise it fails
- If the verification code is entered incorrectly for more than three times, the account will be automatically locked, and the administrator can only log in after unlocking it

#### 4. Administrator login

- Click the login button on the homepage

![image-03](/media/img/managerlogin-en.jpeg){ loading=lazy style="max-width: 100%" }
-
- If you logged in as an administrator last time, click Login this time to jump to the administrator login page
- Administrator and password: Enter the username and password when registering, if they are the same, the login is successful, otherwise it fails

!!! info "User"
     Change user: change the currently logged in user
     View OPENID: View the information used by ordinary users to log in
     Recent Contacts: View a list of five users that the current user has been in contact with recently

#### 5. Report Center

- Visible with Report Center permissions

![image-05](/media/img/chuku-en.png){ loading=lazy style="max-width: 100%" }

- Click Report Center - open the outbound report by default, that is, the data of delivery management, and count the total sales of invoices created within 15 days by default
- Click on the report center - click on the receipt report, that is, the data of the receipt management, the default statistics of the total receipt of the arrival notice created within 15 days
- Click on the report center - click on the receipt and delivery report, that is, all the data of receipt and delivery, and count the number of all receipts and deliveries in the system

#### 6. Receiving Management

- Visible to those who have the authority to operate receipt management

![image-06](/media/img/daohuo-en.jpg){ loading=lazy style="max-width: 100%" }

##### 6.1 Click Receipt Management

- Open the list of arrival notices - add arrival notices

!!! info "ASN"

     Added arrival notice:

     1. Select a supplier name from the list

     2. Enter and select a commodity code

     3. Enter the quantity

![image-07](/media/img/addshouhuo-en.jpeg){ loading=lazy style="max-width: 100%" }

!!! info "Select"

     Get from list of suppliers

     Enter the first few items of data first, and then select one from the results after the search results come out. For example, enter a 00 or a, and the complete product code will pop up. Select one

![image-08](/media/img/mohuchaxunfahuo-en.png){ loading=lazy style="max-width: 100%" }

!!! info "Input"

     Finally, enter the quantity of the product. If you want to add more products, continue to enter the product code in the next line, otherwise click the OK button

     Arrival notice just added, its initial status is pending arrival

##### 6.2 Click Receipt Management

- Open the arrival notice list - change the arrival notice status

![image-09](/media/img/daohuozhuangtai-en.jpg){ loading=lazy style="max-width: 100%" }

- The buttons in the operation column are View Arrival List, Confirm Arrival, Confirm Unloading, Confirm Sorting, Edit and Delete
- Check the delivery note: Check the details of the delivery note, the QR code inside is for the scanner to scan
- Confirm Arrival: Click this item only for the arrival notice in the pending arrival status. After confirmation, the status will change to pending unloading, delete the data of pending arrival, and update the data to pending unloading at the same time.
- Confirm unloading: Click this item only for the arrival notice in the waiting to be unloading state. After confirmation, the status will change to waiting for sorting, delete the data to be unloaded, and update the data to be sorted at the same time.
- Confirm Sorting: Click this item only for the arrival notice in the waiting for sorting state, enter the actual arrival quantity after confirmation, change the status to sorted, delete the data to be sorted, and update the data to sorted at the same time.
- Edit Arrival Notice: Click this item only for the arrival notice in the waiting status, similar to 6.1, otherwise an error message will be returned
- Delete the arrival notice, click this item only for the arrival notice in the waiting state, otherwise an error message will be returned

##### 6.3 Click Receipt Management

- Click Sorted - Product on the shelf

![image-10](/media/img/shangjia-en.jpeg){ loading=lazy style="max-width: 100%" }

- Click on the putway button under the action bar

![image-11](/media/img//shangjia1-en.jpeg){ loading=lazy style="max-width: 100%" }

- Enter the location name: enter the first few items, and select one from the queried list
- Enter the quantity: Enter the number. If it is correct after completion, it will not prompt, delete the data just now in the sorted list, and change the status of the arrival list to receipt completed

#### 7. Delivery management

- Visible with the permission to operate delivery management


![image-12](/media/img/fahuo-en.jpeg){ loading=lazy style="max-width: 100%" }

##### 7.1 Click Shipping Management

- Open the invoice list - add invoice

![image-13](/media/img/addfahuo-en.jpeg){ loading=lazy style="max-width: 100%" }

!!! info "New"

     Add invoice:

     1. Select a customer name from the list

     2. Enter and select a commodity code

     3. Enter the quantity

- Fetch from customer list
- Enter the first few items of data first, and then select one from the results after the search results come out. For example, enter a 00 or a, and the complete product code will pop up, select one

![image-14](/media/img/mohuchaxunfahuo-en.png){ loading=lazy style="max-width: 100%" }

!!! info "Input"

     Finally, enter the quantity of the product. If you want to add more products, continue to enter the product code in the next line, otherwise click the OK button

     The invoice just added, its initial status is pre-shipment

##### 7.2 Click Shipping Management

- Open the list of invoices - change the status of the invoice


![image-16](/media/img/fahuozhuangtai-en.jpeg){ loading=lazy style="max-width: 100%" }

- The buttons in the operation column are check invoice, confirm order, generate picking list, print picking list, confirm picking, loading and delivery, sign receipt, edit and delete buttons
- View invoice: View the details of the invoice, the QR code inside is for the scanner to scan
- Confirm order: Click this item only for invoices in pre-delivery status. After confirmation, the status will change to new invoice, delete the data of the pre-delivery order, and update the data to the new invoice at the same time.
- Generate Picking List: Only click this item for the delivery note in the new delivery order status. If the inventory quantity is sufficient, it will be changed to waiting for picking, delete the data of the new delivery order, and update the data to waiting picking; if the inventory quantity is insufficient, Enter backorders.
- Print Picking List: Click this item only for the invoices that are waiting for sorting, and you can view the details of the picking list. The QR code inside is for the scanner to scan.
- Confirm the completion of picking: click this item only for the invoices in the waiting for sorting state, enter the quantity to be picked, and do not exceed the default value, otherwise an error will be reported. After confirmation, the status will change to picked, and the data to be picked will be deleted , updated to Picked.
- Loading and delivery: click this item only for the invoice in the picked state, otherwise an error message will be returned, please enter a few characters in the driver's name, select one in the pop-up selection box and click OK, the status will change to completed Shipment, delete the picked data, update to shipped.

![image-17](/media/img/siji-en.png){ loading=lazy style="max-width: 100%" }

- Receipt order: Click this item only for delivery orders that have been delivered, otherwise an error message will be returned, please enter the actual quantity of goods and the number of damaged goods, click the OK button, the status will change to signed, and the delivered ones will be deleted The data is updated to sign the receipt.

![image-18](/media/img/qianshou-en.jpeg){ loading=lazy style="max-width: 100%" }

#### 8. Inventory Management

- Visible with inventory management permissions

![image-16](/media/img/kucun-en.jpg){ loading=lazy style="max-width: 100%" }

- Divided into inventory list, storage location list, empty storage location, stock storage location, dynamic inventory and inventory record
- Inventory list: records all product change information
- Location list: records all location change information
- Empty warehouse location: the information of the warehouse location without goods is recorded
- In-stock location: the information of the location where the product information is stored is recorded
- Dynamic inventory: records the product data that has changed within 15 days. After the inventory, the data will enter the inventory record, and there will be no more data in the dynamic inventory.
- Inventory records: record all inventory records in the system, select all corresponding inventory records on the date

#### 9. Finance Center

- Can be seen with permission to operate the financial center

![image-17](/media/img/caiwu-en.jpeg){ loading=lazy style="max-width: 100%" }

- Divided into two sub-modules of fixed assets and freight management
- Fixed assets: record fixed asset information, can add, edit and delete
- Freight management: freight information is recorded, which can be added, edited and deleted

#### 11. Commodity Management

- Can be seen with permission to operate commodity management

![image-18](/media/img/shangpin-en.jpg){ loading=lazy style="max-width: 100%" }

- It is divided into sub-modules such as product list, product unit, product category, product color, product brand, product shape, product specification and product origin, and all sub-modules have add/edit/delete functions.
- Product list: describe product information, including adding/editing/deleting

- Add new product: add product information, enter complete product information, including product code, select supplier and other information, click the OK button after completion

![image-19](/media/img/addgoods-en.jpg){ loading=lazy style="max-width: 100%" }

- Edit product: To edit product information, click Edit, and click the OK button after the modification is complete

![image-20](/media/img/updategoods-en.jpg){ loading=lazy style="max-width: 100%" }

- Delete product: delete product information, confirm deletion

![image-21](/media/img/delete-en.jpg){ loading=lazy style="max-width: 100%" }

- Commodity unit: describe the commodity unit information, including adding/editing/deleting
- New commodity unit: Add commodity unit information, enter commodity unit information, and click the OK button after completion

![image-22](/media/img/addgoodsunit-en.jpg){ loading=lazy style="max-width: 100%" }

- Edit product unit: Click to edit the product unit information, click Edit, and click the OK button after the modification is complete

![image-23](/media/img/updategoodsunit-en.jpg){ loading=lazy style="max-width: 100%" }

- Delete commodity unit: delete commodity unit information, confirm deletion

![image-24](/media/img/delete-en.jpg){ loading=lazy style="max-width: 100%" }

- Commodity category: describe commodity category information, including adding/editing/deleting
- Add a product category: add product category information, enter the product category information, and click the OK button after completion

![image-25](/media/img/addgoodscategory-en.jpg){ loading=lazy style="max-width: 100%" }

- Edit product category: Click to edit the product category information, click Edit, and click the OK button after the modification is complete

![image-26](/media/img/updategoodscategory-en.jpg){ loading=lazy style="max-width: 100%" }

![image-27](/media/img/addgoodscategory-en.jpg){ loading=lazy style="max-width: 100%" }

- Delete product category: delete product category information, confirm deletion

![image-28](/media/img/delete-en.jpg){ loading=lazy style="max-width: 100%" }

- Product color: describe product color information, including add/edit/delete
- Add product color: Add product color information, enter product category information, and click the OK button after completion

![image-29](/media/img/addgoodscolor-en.jpg){ loading=lazy style="max-width: 100%" }

- Edit product color: Click to edit the product color information, click Edit, and click the OK button after the modification is complete
![image-30](/media/img/updategoodscolor-en.jpg){ loading=lazy style="max-width: 100%" }

- Delete product color: delete product color information, confirm deletion

![image-31](/media/img/delete-en.jpg){ loading=lazy style="max-width: 100%" }

- Product brand: describe the product brand information, including adding/editing/deleting
- Add product brand: Add product brand information, enter product brand information, and click the OK button after completion

![image-32](/media/img/addgoodscategory-en.jpg){ loading=lazy style="max-width: 100%" }

- Edit product brand: Click to edit the product brand information, click Edit, and click the OK button after the modification is complete

![image-33](/media/img/updategoodscategory-en.jpg){ loading=lazy style="max-width: 100%" }

- Delete product brand: delete product brand information, confirm deletion

![image-34](/media/img/delete-en.jpg){ loading=lazy style="max-width: 100%" }

- Commodity shape: describe commodity shape information, including add/edit/delete
- Add product shape: add product shape information, enter product shape information, and click the OK button after completion

![image-35](/media/img/addgoodsshape-en.jpg){ loading=lazy style="max-width: 100%" }
-
- Edit product shape: Click to edit the product shape information, click Edit, and click the OK button after the modification is complete

![image-36](/media/img/updategoodsshape-en.jpg){ loading=lazy style="max-width: 100%" }

- Delete product shape: delete product shape information, confirm deletion

![image-37](/media/img/delete-en.jpg){ loading=lazy style="max-width: 100%" }

- Commodity specification: describe commodity specification information, including add/edit/delete
- Add product specifications: Add product specification information, enter product specification information, and click the OK button after completion

![image-38](/media/img/addgoodsspecification-en.jpg){ loading=lazy style="max-width: 100%" }

- Edit product specifications: Click to edit the product specification information, click Edit, and click the OK button after the modification is complete

![image-39](/media/img/updategoodsspecification-en.jpg){ loading=lazy style="max-width: 100%" }

- Delete product specification: delete product specification information, confirm deletion

![image-40](/media/img/delete-en.jpg){ loading=lazy style="max-width: 100%" }

- Commodity origin: describe the commodity origin information, including adding/editing/deleting
- Add commodity origin: Add commodity origin information, enter commodity origin information, and click the OK button after completion

![image-41](/media/img/addgoodsplace-en.jpg){ loading=lazy style="max-width: 100%" }

- Edit product origin: Click to edit the product origin information, click Edit, and click the OK button after the modification is complete

![image-42](/media/img/updategoodsplace-en.jpg){ loading=lazy style="max-width: 100%" }

- Delete product origin: delete product origin information, confirm deletion

![image-43](/media/img/delete-en.jpg){ loading=lazy style="max-width: 100%" }

#### 10. Basic Management

- Visible with permission to operate basic management

![image-45](/media/img/jiben-en.jpg){ loading=lazy style="max-width: 100%" }

- Contains basic configuration information, including company information, supplier information and customer information
- Company information, including adding, editing and deleting
- Add company information: enter the company name/city/address/contact information/person in charge information, and click the confirm button

![image-46](/media/img/company-en.jpg){ loading=lazy style="max-width: 100%" }

- Supplier information, including adding, editing and deleting
- Add supplier information: enter company name/city/address/contact information/person in charge, and click the confirm button

![image-47](/media/img/supplier-en.jpg){ loading=lazy style="max-width: 100%" }

- Customer information, including adding, editing and deleting
- Add customer information: enter customer name/city/address/contact information/person in charge, and click the confirm button

![image-48](/media/img/customer-en.jpg){ loading=lazy style="max-width: 100%" }

#### 11. Warehouse management

- Visible with permission to operate warehouse management
- Contains warehouse settings, location settings, location dimensions and location attributes

![image-49](/media/img/warehouse-en.jpg){ loading=lazy style="max-width: 100%" }

- Warehouse settings, including adding, editing and deleting
- New warehouse: Enter the warehouse name/city/address/contact information/person in charge information, click the confirm button

![image-50](/media/img/addwarehouse-en.jpg){ loading=lazy style="max-width: 100%" }

- Location setting, including adding, editing and deleting
- New location: Enter the name of the location, select the size of the location and the attribute of the location. The attribute of the location must be selected as a normal attribute before it can be put on the shelf. Click the confirm button

![image-51](/media/img/addplace-en.jpg){ loading=lazy style="max-width: 100%" }

- Location size, including adding, editing and deleting

![image-52](/media/img/addchicun-en.jpg){ loading=lazy style="max-width: 100%" }

#### 12. Driver Management

- Visible with the permission to operate driver management
- Including driver management, delivery records
- Driver management, including adding, editing and deleting

![image-53](/media/img/driver-en.jpg){ loading=lazy style="max-width: 100%" }

- Add a new driver: enter the driver's name, license plate number and contact information, and click the confirm button

![image-54](/media/img/adddriver-en.jpg){ loading=lazy style="max-width: 100%" }

- Pickup records showing the relationship between the driver and the invoice

![image-55](/media/img/tihuo-en.jpg){ loading=lazy style="max-width: 100%" }

#### 13. Upload Center

- Can be seen with permission to operate the upload center
- Including initial upload and new upload two sub-modules
- Both sub-modules have template download and file upload functions

![image-56](/media/img/upload-en.jpg){ loading=lazy style="max-width: 100%" }

- Initial upload: Use this function to initialize some data when the system is just deployed
- New upload: When the system already has some data, use new upload to continue adding data in order not to overwrite the original data
- Template download: you can download customer templates/supplier templates/commodity templates, and support xlsx format
- File upload: click the plus sign, select the corresponding template, and click the OK button


![image-58](/media/img/fullupload-en.jpg){ loading=lazy style="max-width: 100%" }

#### 14. Download Center

- Visible with permission to operate the download center
- Download the arrival notice/delivery note/inventory table/location table/commodity table within a certain time range

![image-59](/media/img/download-en.jpg){ loading=lazy style="max-width: 100%" }

- Support downloading the details and overview of the arrival list/shipment note within a certain time range
- Download in csv format

#### 15. User Center

- Visible with the permission to operate the user center
- Contains employee list, captcha and employee type


![image-61](/media/img/user-en.jpg){ loading=lazy style="max-width: 100%" }

- Employee list: Indicates the collection of information for all users subordinate to a unique openid, including modifying user information, locking users, and deleting users
- Verification code: including information necessary for ordinary users to log in
- Employee type: the data that comes with the system, displaying the account type
