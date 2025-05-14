import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from std_msgs.msg import Int32MultiArray, Bool

import pexpect

class PolarH10Reader(Node):
    def _set_up_params(self):
        # MAC ADDRESS
        self.mac_address = self.get_parameter_or(
                "mac_address",
                Parameter("", value="E2:74:8D:5C:73:8A"), # "EB:0B:03:5B:34:34"),
            ).get_parameter_value().string_value
        
        # HRV TOPIC
        # STATUS TOPIC
        
    def __init__(self):
        self.package_name = "ros2_polar_h10"
        
        super().__init__("polar_h10_reader")
        
        self._set_up_params()
        
        self.sensor_status = 0
        
        self.publisher = self.create_publisher(
            Int32MultiArray, "/polar_h10/hrv", 10
        )   
        
        self.subscriber = self.create_subscription(Bool, "/polar_h10/status", self._state_callback, 10) # Tu a che servi?!?!!?
        
        self._read_data()
        
        
    def _state_callback(self, msg):
        self.sensor_status = msg.data

    def _read_data(self):
        # SENSOR CONNECITON
        sensor_connection = True
        
        while sensor_connection:
            gatt = pexpect.spawn("gatttool -t random -b " + self.mac_address + " --char-write-req --handle=0x0011 --value=0100 --listen") # gatttool is deprecated. 
            # print(gatt.readline())
            if gatt.readline() == b"Characteristic value was written successfully\r\n":
                line = gatt.readline()
                data = line.split(b" ")
                print(data)
                if data[5] == b"10":
                    self.get_logger().info(f"Sensor [{self.mac_address}] connecting.")
                    sensor_connection = False
            else:
                self.get_logger().error(f"Sensor [{self.mac_address}] connection failed.")        
                
        self.get_logger().info(f"Sensor [{self.mac_address}] connected.")
    
        # DATA READING
        while True:
            line = gatt.readline()
            
            data = line.split()
            print(data)
            if data[5] != b"00":
                hrv = int(data[6], 16)
                ibi = int(data[7], 16)
                battery = int(data[8], 16)
                
                # print(f"{hrv} \t {ibi} \t {battery} \t {self.sensor_status}")
                # print(data)
                
                # if self.sensor_status == True: # TODO tu a che servi? 
                #    self.publisher.publish([hrv, ibi, battery])
                
                self.publisher.publish(Int32MultiArray(data=[hrv, ibi, battery]))
                    
def main(args=None):
    rclpy.init(args=args)
    
    polar_h10_reader = PolarH10Reader()
    
    rclpy.spin(polar_h10_reader)
    rclpy.shutdown()
    
if __name__ == "__main__":
    main()
            
        
        