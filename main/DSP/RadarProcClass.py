class Radar(object):
    def __init__(self, radar, samplingRate):
        self.radar = [radar[i][0] for i in range(0, len(radar))]
        self.time = [radar[i][1] for i in range(0, len(radar))]
        self.samplingRate = samplingRate
        self.p = 5
        self.nfft = 512
        self.list = []
        self.cutoff = 2
        self.radarobj = None
        self.order = 6

    def getVariables(self):
        return self.samplingRate, self.radar, self.time

    def main(self):
        radar, time = self.slidingwindow()
        fft = self.fft(radar)
        peakY = np.max(fft[1])  # Find max peak
        locY = fft[0][np.argmax(fft[1])]  # Find its location
        return {
            'fft': fft,
            'peak': peakY,
            'loc': locY
        }

    def slidingwindow(self):

        if (len(self.radar) == 2500):
            overlap = 0.4

            nw = 250
            ns = int(nw * (1.0 - overlap))
            n0 = 0
            n1 = n0 + nw
            N = len(self.radar)

            counter = 0
            counter1 = 1

            SNR = 0
            bestwin = 0
            besttime = 0
            while True:
                data = self.radar[n0:n1]
                time = self.time[n0:n1]
                array = Radar.HanningFunction(data)
                filtered_data = Radar.butter_lowpass_filter(array, self.cutoff, self.samplingRate, order=self.order)
                corrMtrx = self.getcorrMtrx(x=filtered_data, m=35)
                frequency, psd, eigenvals = self.musicAlg(corrMtrx)
                currSNR = sum(eigenvals[0:self.p]) / sum(eigenvals[self.p: len(eigenvals)])
                if (currSNR > SNR):
                    SNR = currSNR
                    bestwin = filtered_data
                    besttime = time
                # r = counter // n
                # c = counter % n
                # ax[r][c].plot(eigenvals)
                # ax[r][c + 1].plot(xf, yf)
                n0 += ns
                n1 += ns
                counter += 2
                counter1 += 1
                if n1 > N:
                    break

            return bestwin, besttime
        else:
            print("Error your data vector is not the proper length")

    def diffCalc(self, list1):
        list2 = []
        for i in range(1, len(list1)):
            list2.append(list1[i] - list1[i - 1])
        return list2

    def fft(self, array):
        yf = fft(array, n=self.nfft)
        xf = np.linspace(0.0, self.samplingRate / 2, self.nfft / 2)
        return xf, abs(yf[0:self.nfft / 2])

    def HanningFunction(radarData):
        return radarData * np.hanning(len(radarData))

    def getcorrMtrx(self, x, m):
        x = np.array(x)
        m = m
        N = len(x)
        xlen = m + 1
        rowVector = x[N - xlen: N]
        columnVector = x[0: N - m]
        hanMatrix = hankel(c=np.array(columnVector).T, r=rowVector)
        X_unscaled = np.fliplr(hanMatrix)
        X = X_unscaled / np.sqrt(N - m)
        Xnew = np.conj(np.fliplr(X))
        corrMatrix = np.vstack((X, Xnew)) / np.sqrt(2)
        return corrMatrix

    def musicAlg(self, corrMtrx):
        u, s, v = np.linalg.svd(corrMtrx)

        self.nfft = 512

        frequencyVector = np.linspace(0, 1, self.nfft // 2)
        frequencyVector *= self.samplingRate / 2

        sum = 0
        for i in range(self.p, len(v)):
            y = fft(v[i], n=self.nfft)
            sum += abs(y) ** 2 / s[i]

        sum = 1 / sum

        sum = sum[0:self.nfft // 2]

        return frequencyVector, sum, s

    def graphFilterResults(self):
        order = 6
        cutoff = 2

        b, a = Radar.butter_lowpass(cutoff, self.samplingRate, order)

        w, h = freqz(b, a, worN=8000)
        plt.subplot(2, 1, 1)
        plt.plot(0.5 * self.samplingRate * w / np.pi, np.abs(h), 'b')
        plt.plot(cutoff, 0.5 * np.sqrt(2), 'ko')
        plt.axvline(cutoff, color='k')
        plt.xlim(0, 0.5 * self.samplingRate)
        plt.title("Lowpass Filter Frequency Response")
        plt.xlabel('Frequency [Hz]')
        plt.grid()

        y = Radar.butter_lowpass_filter(self.radar, cutoff, self.samplingRate, order)

        plt.subplot(2, 1, 2)
        plt.plot(self.time, self.radar, 'b-', label='data')
        plt.plot(self.time, y, 'g-', linewidth=2, label='filtered data')
        plt.xlabel('Time [sec]')
        plt.grid()
        plt.legend()

        plt.subplots_adjust(hspace=0.35)
        plt.show()
        return y

    def butter_lowpass(cutoff, fs, order=5):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        return b, a

    def butter_lowpass_filter(data, cutoff, fs, order=5):
        b, a = Radar.butter_lowpass(cutoff, fs, order=order)
        y = lfilter(b, a, data)
        return y

    def testSpectrum(self, data):
        corrMtrx = self.getcorrMtrx(data, 30)
        return self.musicAlg2(corrMtrx)

    def musicAlg2(self, corrMtrx):
        u, s, v = np.linalg.svd(corrMtrx)
        self.nfft = 512
        frequencyVector = np.linspace(0, 1, self.nfft // 2)
        frequencyVector *= self.samplingRate / 2
        sum = 0
        for i in range(self.p, len(v)):
            y = fft(v[i], n=self.nfft)
            sum += abs(y) ** 2 / s[i]

        sum = 1 / sum

        sum = sum[0:self.nfft // 2]

        return frequencyVector, sum, s
