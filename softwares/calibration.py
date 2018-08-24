import Adafruit_PCA9685
import time

def _map(x, a, b, c, d):
    return (x - a) * (d - c) / (b - a) + c

def main():
    print('angles are in between -6000 and +6000 ...')
    print('servos are in between 1 and 12 ...')
    print('to set the angle, write +x to increment by x and -x to decrement')
    print('after finding the write angle, write \'ok\'')
    print('to exit after calibrating every servo, write \'exit\'')
    print('\n')

    time.sleep(.5)

    print('creating PCA9685 device with a PWM frequency of 50Hz ...')
    device = Adafruit_PCA9685.PCA9685()
    device.set_pwm_freq(50)
    print('done')
    print('\n')
    print('\n')

    with open('calibration.txt', 'w+') as conf:
        table = [ 0 for i in range(12) ]

        for i in range(12):
            device.set_pwm(i, 0, 0)

        while True:
            servo = raw_input('choose servo: ')

            if servo == 'exit':
                break
            elif int(servo) < 1 or int(servo) > 12:
                print('invalid servo ({})'.format(servo))
                continue

            angle = 0
            while True:
                inp = raw_input('angle({}) :> '.format(angle))

                if int(inp[1:]) > 6000 or int(inp[1:]) < -6000:
                    print('invalid angle ({}) ...'.format(inp[1:]))
                    continue

                if inp == 'ok':
                    table[int(servo)] = angle
                    break

                if inp[0] == '+':
                    angle += int(inp[1:])
                else:
                    angle -= int(inp[1:])

                print('setting servo ({}) to angle ({})'.format(servo, angle))
                #type(angle)
                device.set_pwm(servo, 0, int(_map(angle, -4500, 4500, 204.8, 409.6)))

        print('writing angles to the calibration.txt file ...')
        for i in range(table):
            print('servo ({}) angle ({})'.format(i + 1, table[i]))
            conf.write('{} {}'.format(i + 1, table[i]))
        print('done')
        return

if __name__ == '__main__':
    main()
