# Test Dataset for Prompt Validation

## Known Diagnoses (from user examples)

### Test Case 1
**Statement**: "I'm feeling all consumed and obsessed by this other person's presence. I'm worried that I'm slipping into like old patterns of giving way more than I'm actually receiving. And I feel really vulnerable. I feel like, like I can't even focus on anything else. And I'm like, scared for my little heart, like, I want to guard my little heart, because it's like, this outside entity is just like, please is, like, this big. Big, bad, scary, death, like sucking my life force energy. But I want it to be different. I want it to just be pure love, like what is which is also what I'm sensing at the same time."

**Known Diagnosis**: Omnipotent, Frustrated, Premature, Constricted, Floaty

**Expected Top 3**: Omnipotent (highest), Premature (high), Constricted or Floaty

---

### Test Case 2
**Statement**: "Um, so I just started dating this person, and it's like, triggered me, because I'm feel so anxious about, like, what's going to happen? Does he like me? It's really, like, destabilizing, and I don't like seeing that old behavior in me activated. I feel like, really needy and like Bucha. Trying to hide the fact that I'm needy and so uncomfortable in my body, and like, foggy, and like, just Yeah, consumed by it, and like, I'm thinking about it all the time, and like it's robbing me from my center."

**Known Diagnosis**: Omnipotent, Symbiotic, Frictive, Deprived, Floaty, Flighty, Constricted

**Expected Top 3**: Frictive (highest - consumed, thinking about it all time), Omnipotent (high - destabilizing, robbing from center), Symbiotic (does he like me)

---

### Test Case 3
**Statement**: "Okay, so back in August, I noticed that there was bubbling paint on my car in several different places, so I looked it up online for that model of car, and it said that it's an issue with that car. So I went to the dealership and I went. I took the car to the dealership where I bought it, and I showed them the paint, and they said that, yes, it is a problem, but that they don't fix it there, but they could file a claim with Jeep for me, since the car was still under warranty. So that was in August, and they told me that it might take a couple of months for me to hear back from them. So I checked in with them after a couple of months, and they told me there was still a couple of people ahead of me. And. Then I brought my car to be serviced another time and asked again. Following that, I got an email asking about my experience with the dealership, and if I had any issues. I shared the issue with the president of the company, and they said, although they couldn't help me, they would have somebody contact me. And that didn't happen. So I went there today to drop off my car for an oil change, and I asked about the problem again, and they again told me that there's two people ahead of me and that I will hear from them when they hear back from Jeep."

**Known Diagnosis**: Disconnected, Frustrated, Sacrificing

**Expected Top 3**: Frustrated (blocked, things not working), Sacrificing (being put off, not prioritized), Disconnected (describing events without emotional reaction - reporting pattern)

---

### Test Case 4
**Statement**: "So I'm really struggling to be present. Currently, I find myself thinking about all of these things happening in the future and all these problems that I want to take care of, and all these things that I want to..I find myself being in the future a lot and focusing a lot on things that are coming up, focusing on other people's problems that I want to help them with my own challenges that I want to resolve instead of actually taking care of it in the moment, I'm just ruminating and thinking about ways that I can potentially do that in the future. So, yeah, just trying to understand what that's about and noticing the places in my day to day life, in my conversations and relationships where I'm already thinking ahead to the next thing or to solutions and not so much being in the moment."

**Known Diagnosis**: Frustrated, Floaty, Constricted, Premature, Omnipotent

**Expected Top 3**: Floaty (not present, in the future), Premature (other people's problems I want to help), Omnipotent or Constricted (fix-it mentality, ruminating)

---

### Test Case 5
**Statement**: "So I have to really adult right now in my life. I have to rent a car, buy a car, and I have to book a flight, and the airport I want to book from isn't having flights when I need the flight, so I'm gonna have to go to another airport and, like, all these kind of technical need to sit down. Like, plan adult, be responsible. Choose. So, yeah, there's things I need to do that are adulting. I need to rent a car. I need to buy a car, mostly. And every time I need to really decide I feel resistance, so then I kind of avoid it, because it feels like a really big responsibility. And so instead, I think, okay, I'll just rent a car, and then when I try to rent a car, it doesn't work. Something's not working in the system. I can't and then I feel I can't figure this out. It's too adulty for me, and I get kind of frustrated, I guess. And then also with a flight, I need to book a flight at a certain date, and those dates are not available in the nearest airport, so I have to, like, sit down and plan a different route, yeah."

**Known Diagnosis**: Indulged, Frustrated, Disconnected

**Expected Top 3**: Indulged (highest - "too adulty," resistance to adult tasks), Frustrated (it doesn't work, can't figure it out), Disconnected (systems feel foreign)

---

## Evaluation Metrics

For each test case, measure:

1. **Precision**: Did it identify the known diagnoses?
2. **Ranking**: Are the top matches in the expected order?
3. **False Positives**: Did it add styles that weren't diagnosed?
4. **Confidence Calibration**: Do confidence scores match accuracy?

### Scoring System
- **Perfect Match**: All known diagnoses identified with correct relative ranking = 10 points
- **Partial Match**: Top 3 correct but missing some from full diagnosis = 7 points
- **Weak Match**: At least 2 correct in top 5 = 4 points
- **Miss**: Fewer than 2 correct = 0 points

### Pass Threshold
- Average score ≥ 7.0 across all test cases = Production ready
- Average score 5.0-6.9 = Needs refinement
- Average score < 5.0 = Rethink approach

