// Lab05vst.java
// This is the student, starting version of the Lab05 assignment.


import java.awt.*;
import java.applet.*;


public class Lab05vst extends Applet
{
    public void paint(Graphics g)
    {
        int width = 980;
        int height = 630;
        int x1 = 10;
        int y1 = 640;
        int x2 = 990;
        int y2 = 640;
        g.drawRect(10,10,width,height);

        //bottom-left
        for (int i = 0; i < 300; i +=10){

            g.drawArc(0, y1, 445+i,320, 0, 270);
        }
        //bottom-right

        //top right

        //top-left
    }
}

