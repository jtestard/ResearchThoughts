# Introduction

The introduction should give the setting of the research exam and expose the problem we are trying to solve. It must :

 1. Explain the background and emergence of the Polyglot Persistence problem.
 - Go over the challenges the problem impose
 - Introduct a running example to be used throughout the survey

### Running Example

Our running example is an e-commerce website.

New e-commerce website is evaluating it's storage needs given the features it wishes to provide its customers.

Consider the situation of an e-commerce startup who just received the funding they required and wish to implement their data infrastructure. They have come up with a list of features their application should provide : 

The product manager has a very ambitious vision of what information customers can specify about themselves and other customers (preferences, ratings...) but isn't quite sure about the specifics, thus he expects the schema representing customers to vary significantly over the next few months. The products specifics are expected to vary significantly as well.

Like any other e-commerce website, customers can shop through the website using a shopping cart and finalize their purchase through a check out page. The shopping cart is transient and doesn't need to be stored after the purchase is finalized, but must always be quickly available. Customers can purchase items with store credits and the products managers are very careful about the integrity of the customer's store credit balance, thus want guarantees that its value will be immediately accurate after any finalized purchase, even if that means the customers has to wait a few milliseconds longer.

The entrepreneurs also imagine customers importing their friends from Facebook or other social networks, or make contacts on their own through the website. Such social information could then by used to provide recommendations to customers when they are browsing such as "your friends bought these accessories for this product".

Finally, the entrepreneurs want to understand better their clients. In the context of behavioral targeting, they wish to aggregate their user's unique clicks over the past hour, updated every 5 minutes. The number of clicks is expected to be very big, although loosing clicks isn't considered a big problem.



This website has :

 - customers : need flexibility. User information is quite varied (votes, compliments) and not completed fixed by the product managers.
 - products: likewise for product information.
 - shopping cart : transient objects on which customers place their items.
 - orders : order information is expected to be analyzed to predict customer trends using warehousing tools.
 - friendship relationships among customers (through a social network).
 - user activity is constanty monitored through user activity logs.

Queries :

 - Product browsing and purchase; involves customers, products, shopping cart and orders.
 - Product recommendation based on social network.
 - User activity over the past month is aggregated every hour.

Stores :

 - RDBMS for analytics on customer purchases (orders).
 - Key-value store for customer shopping cart.
 - Graph store for social network
 - MongoDB for customers and products
 - HBase for storing the activity logs
 - Storm to perform the user activity monitoring 
 



### Challenges

#### How to choose which systems to integrate given a set of requirements?

 - There is a wide variety of systems.
 - Multiple systems may fit the primary need of an application.
 - How to decide between a SQL or NoSQL system
 - Especially when application isn't well defined, benchmarking is not easy.
 - We will view a number of tools suggested as a solution, which were previously surveyed by. 

#### Integrating multiple specialized system into a PP system

 - Each system was built independantly and provide their own query interface, query language, data model.
 - The polyglot persistence, in order to provide 
 - Architectural question : how are we going to link those heterogeneous.

#### Optimizing Queries

#### Deploying subsystems

 - Some specialized systems are meant to be deployed on clusters while others are meant to be deployed on individual machines.
 - Should the developer of the PP system choose to deploy his subsystems on a common cluster which she owns or deploy each subsystem on a Platform-as-a-Service (PaaS) owned by a third party, or a mixture of both?
 - Should she choose a common cluster, how can she allocate resources to individual subsystems?
 - Some subsystems (especially those coming from the Hadoop ~\cite{Shvachko2010} ecosystem) separate their storage and compute components. Should the use  

#### Updating the PP system while keeping it available and consistent

 - Updating data in any database systems poses the problem of consistency guarantees in the presence of multiple concurrent updates.
 - The CAP theorem states that a distributed system can either be immediately consistent or always available, but not both.
 - In the case of polyglot persistence, this means if an update to multiple subsystems has to be immediately consistent, then the PP system won't be available until all of the subsystems involved have been properly updated.
 - Moreover, the subsystems themselves may have different consistency/availability tradeoffs which may have to be reconciled. 
 - How can we describe the availability and consistency characteristics of a PP system?
 
#### Concerns :

 - mixing requirements (what the PP system needs to do) with challenges (what problems occur when designing a PP system) and solutions (how the PP system can achieve the requirements given the challenges).
 - cloud computing is an important paradigm in PP but hasn't been discussed.
 - language should be declarative but we don't explain why.
 - conflict between opportunity of some specialized PP systems which can't apply in a general solution. 

### Example from Yupeng

*It is widely believed that mobile will be the future of IT. As tablets and smartphones go places on the sales front, the increasing demand for mobile applications is happening on the development side too. A recent survey from IBM [40] found that the number of developers working on mobile application will tremendously increase in the future.*

<span style="color:red">
In this paragraph, Yupeng shows there is interest for his topic (mobile web applications) in the development community.
</span>

#### Mobile native applications and web applications

*Mobile applications are classified into two categories: mobile native applications and mobile web applications. A native application is specifically designed to run on a device’s operating system and machine firmware, such as iPhone and Android, and typically needs to be adapted/adjusted for different devices; while a web application, or browser application, is one in which all or some parts of the software are downloaded from the Web each time it runs in the browser, and it can usually be accessed from all Web-capable mobile devices.*
*Traditionally native applications are superior in terms of performance and the only means to access device attributes such as geolocation API and camera. And web applications are favored by the developers for their cross-platform compatibility and the ability to update and maintain without distributing and installing software. Although native applications are argued to be necessary for certain types of apps, such as high- quality games, for many other types of applications, the economics of mobile software development and publishing favors the mobile web. Taptu [1] reports that by the end of year 2009 there are 326,000 Mobile Touch Web sites worldwide, comparing to 148,000 iPhone apps in the App Store and 24,000 apps in the Android market.*

<span style="color:red">
Compare and constract native and web mobile applications.
</span>
*Moreover, The browser-based mobile web market is expected to grow much faster than the native app market, as the user experiences provided by both types of applications are increasingly blurred due to HTML5 being more and more popular. With the support for HTML5, the platform-independent open standard, being rolled out in most browsers, it is getting easier and easier for the developers to create rich user experiences with the mobile browser without having to create platform-specific applications. These features include (1) client-side local storage and files cache for offline support, which we will address in details in section 3.1; (2) APIs that gaining direct access to the hardware (camera, GPS,etc) (3) more markup formats to improve mobile web applications, for instance, the email input type that mobile browsers could customize their onscreen keyboard to make it easier to type email addresses. Today, there are already some good examples of mobile web applications utilizing HTML5 features, including mobile Gmail, Google Maps, and navigation apps.*