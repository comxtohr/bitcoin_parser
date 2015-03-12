import sys
import time
import struct
import datetime

def uint8_t(stream):
  return ord(stream.read(1))

def uint16_t(stream):
  return struct.unpack('H', stream.read(2))[0]

def uint32_t(stream):
  return struct.unpack('I', stream.read(4))[0]

def uint64_t(stream):
  return struct.unpack('Q', stream.read(8))[0]

def hash32(stream):
  return stream.read(32)[::-1]

def varint(stream):
  size = uint8_t(stream)
  if size < 0xfd: return size
  if size == 0xfd: return uint16_t(stream)
  if size == 0xfe: return uint32_t(stream)
  if size == 0xff: return uint64_t(stream)

def magicid(stream):
  buf = stream.read(4)
  if buf == '':
    return -1
  else:
    return struct.unpack('I', buf)[0]

def script(stream, length):
  return stream.read(length)

def scriptstr(buf):
  return ''.join(('%.2x' % ord(i)) for i in buf)

def hashstr(buf):
  return ''.join(('%.2x' % ord(i)) for i in buf)

def timestr(buf):
  return datetime.datetime.fromtimestamp(buf)

total = 0
starttime = time.clock()
with open (sys.argv[1],'rb') as f:
  while True:
    magicID = magicid(f)
    if magicID == -1:
      break
    else:
      total += 1
    headerLength = uint32_t(f)
    versionNumber = uint32_t(f)
    prevHash = hash32(f)
    merkleRoot = hash32(f)
    timeStamp = uint32_t(f)
    difficulty = uint32_t(f)
    nonce = uint32_t(f)
    transactionCount = varint(f)  
    print 'magicID:', magicID
    print 'headerLength:', headerLength
    print 'versionNumber:', versionNumber
    print 'prevHash:', hashstr(prevHash)
    print 'merkleRoot:', hashstr(merkleRoot)
    print 'timeStamp:', timestr(timeStamp)
    print 'difficulty:', difficulty
    print 'nonce:', nonce
    print 'transactionCount:', transactionCount
    print '=============Transaction============='
    for i in range(transactionCount):
      transactionVersionNumber = uint32_t(f)
      inputCount = varint(f)
      print 'transactionVersionNumber:', transactionVersionNumber
      print 'inputCount:', inputCount
      print '---------------Input---------------'
      for j in range(inputCount):
        transactionHash = hash32(f)
        transactionIndex = uint32_t(f)
        scriptLength = varint(f)
        inputScript = script(f, scriptLength)
        sequenceNumber = uint32_t(f)
        print 'transactionHash:', hashstr(transactionHash)
        print 'transactionIndex:', ('%x' % transactionIndex)
        print 'scriptLength:', scriptLength
        print 'inputScript:', scriptstr(inputScript)
        print 'sequenceNumber:', ('%x' % sequenceNumber)
        print '-----------------------------------'
      outputCount = varint(f)
      print 'outputCount:', outputCount
      print '--------------Output---------------'
      for j in range(outputCount):
        value = uint64_t(f)
        outputScriptLength = varint(f)
        outputScript = script(f,outputScriptLength)
        print 'value:', value
        print 'outputScriptLength:', outputScriptLength
        print 'outputScript', scriptstr(outputScript)
        print '-----------------------------------'
      transactionLockTime = uint32_t(f)
      print 'transactionLockTime:', transactionLockTime
      print '==================================='
endtime = time.clock()
print 'total:', total
print 'runtime:', endtime - starttime
