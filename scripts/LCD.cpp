
const String LCD_MATERIAL_NAME_PREFIX = "lcd_digit";

struct LCDImpl
{
    EnvironmentClient *c;
    StringList digits;

    LCDImpl(EnvironmentClient *client)
    {
        c = client;
    }
    void locateDigitNodesOnce()
    {
        // Only do it once.
        if (!digits.empty())
            return;
        // Children are digits.
        digits = c->get("node.$SCENE.$NODE.children");
    }
    void setDigitValue(u32 digitID, const String &value)
    {
        c->setConst("DIGIT", digits[digitID]);
        String material = LCD_MATERIAL_NAME_PREFIX + value;
        c->set("node.$SCENE.$DIGIT.material", material);
    }
    void setValue(const StringList &key, const StringList &value)
    {
        locateDigitNodesOnce();
        String strval = value[0];
        // Display nothing if:
        // * Value is longer than we can display.
        // * Value is none.
        if ((strval.length() > digits.size()) ||
            !strval.length())
        {
            for (u32 i = 0; i < digits.size(); ++i)
                setDigitValue(i, "");
            return;
        }
        // Divide string value into separate digits.
        // Use empty value for padded digits.
        u32 start = digits.size() - strval.length();
        for (u32 i = 0; i < digits.size(); ++i)
            // Digit.
            if (i > = start)
                setDigitValue(i, strval[i - start]);
            // Padding.
            else
                setDigitValue(i, "");
    }
}

struct LCD
{
    EnvironmentClient *c;
    LCDImpl *impl;

    LCD(const String &sceneName,
        const String &nodeName,
        Environment *env)
    {
        c = new EnvironmentClient(env, "LCD/" + nodeName);
        impl = new LCDImpl(c);
        c->setConst("SCENE", sceneName);
        c->setConst("NODE",  nodeName);
        c->provide("lcd.$SCENE.$NODE.value", MJIN2_EPS(impl->setValue));
    }
    ~LCD()
    {
        delete impl;
        delete c;
    }
}

Script *SCRIPT_CREATE(const String &sceneName,
                      const String &nodeName,
                      Environment *env)
{
    return new LCD(sceneName, nodeName, env);
}

void SCRIPT_DESTROY(Script *script)
{
    delete script;
}

