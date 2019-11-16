#include <ros.h>
#include<geometry_msgs/Twist.h>
#include<geometry_msgs/Point.h>

ros::NodeHandle  nh;

geometry_msgs::Twist data;
geometry_msgs::Point voltage;

ros::Publisher datapub("encoder_data", &data);
ros::Publisher voltagepub("battery_data", &voltage);

void setup()
{ 
Serial.begin(115200);
pinMode(1,INPUT);
pinMode(2,INPUT);
pinMode(3,INPUT);
pinMode(4,INPUT);
pinMode(5,INPUT);
pinMode(6,INPUT);
pinMode(7,INPUT);
pinMode(8,INPUT);

nh.initNode();

nh.advertise(datapub);
nh.advertise(voltagepub);

}

void loop()
{
float len[8];
float scale_1,scale_2,scale_3,zener_1,zener_2,zener_3;
len[0]=(analogRead(0)*(0.4/1000)-0.2);              //prism1
len[1]=(analogRead(1)*(0.2/1000)-0.17);             //prism2
len[2]=(analogRead(2)*(6.28/1000)-3.14);            //rot1
len[3]=(analogRead(3)*(3.14/1000)-3.14);            //rot2
len[4]=(analogRead(4)*(6.28/1000));                 //cont
len[5]=((analogRead(5)*scale_1)+zener_1);           //Battery_1=12v
len[6]=((analogRead(5)*scale_2)+zener_2);           //Battery_2=12v
len[7]=((analogRead(5)*scale_3)+zener_3);           //Battery_3=12v

//encoder_data  
data.linear.x=len[0];
data.linear.y=len[1];
data.linear.z=len[2];
data.angular.x=len[3];
data.angular.y=len[4];

//battery_data
voltage.x=len[5];
voltage.y=len[6];
voltage.z=len[7];

datapub.publish(&data);
voltagepub.publish(&voltage);

nh.spinOnce();
 
}
